#include <ctype.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

#include "ippi.h"

#define M_PI 3.14159265358979323846

struct
{
    int row;
    int coloumn;
} zig_zag[8 * 8] =
{
    { 0, 0 },
    { 0, 1 },{ 1, 0 },
    { 2, 0 },{ 1, 1 },{ 0, 2 },
    { 0, 3 },{ 1, 2 },{ 2, 1 },{ 3, 0 },
    { 4, 0 },{ 3, 1 },{ 2, 2 },{ 1, 3 },{ 0, 4 },
    { 0, 5 },{ 1, 4 },{ 2, 3 },{ 3, 2 },{ 4, 1 },{ 5, 0 },
    { 6, 0 },{ 5, 1 },{ 4, 2 },{ 3, 3 },{ 2, 4 },{ 1, 5 },{ 0, 6 },
    { 0, 7 },{ 1, 6 },{ 2, 5 },{ 3, 4 },{ 4, 3 },{ 5, 2 },{ 6, 1 },{ 7, 0 },
    { 7, 1 },{ 6, 2 },{ 5, 3 },{ 4, 4 },{ 3, 5 },{ 2, 6 },{ 1, 7 },
    { 2, 7 },{ 3, 6 },{ 4, 5 },{ 5, 4 },{ 6, 3 },{ 7, 2 },
    { 7, 3 },{ 6, 4 },{ 5, 5 },{ 4, 6 },{ 3, 7 },
    { 4, 7 },{ 5, 6 },{ 6, 5 },{ 7, 4 },
    { 7, 5 },{ 6, 6 },{ 5, 7 },
    { 6, 7 },{ 7, 6 },
    { 7, 7 }
};


struct int_triplet
{
    int prvi;
    int drugi;
    int treci;
};

struct ppm_data
{
    char file_type[3];
    int sirina;
    int visina;
    int max_vrijednost;
    struct int_triplet* rgb_data;
};

void free_ppm_data(struct ppm_data* data_ptr);

struct double_blok
{
    float prvi[8][8];
    float drugi[8][8];
    float treci[8][8];
};

struct ycbcr_blok_data
{
    int sirina;
    int visina;
    struct double_blok* blokovi;
};

void free_ycbcr_blok_data(struct ycbcr_blok_data* data_ptr);

struct ycbcr_blok_data encode(char* filename);

void write_to_file(struct ycbcr_blok_data* ycbcr, char* filename);

int main(int argc, char** argv)
{
    if(argc == 1)
    {
        fprintf(stderr, "filename not specified\n");
        return EXIT_FAILURE;
    }
    struct ycbcr_blok_data encoded_data = encode(argv[1]);
    write_to_file(&encoded_data, "out.txt");
    free_ycbcr_blok_data(&encoded_data);
    return 0;
}

void free_ppm_data(struct ppm_data* data_ptr)
{
    free(data_ptr->rgb_data);
    data_ptr->rgb_data = NULL;
}

void free_ycbcr_blok_data(struct ycbcr_blok_data* data_ptr)
{
    free(data_ptr->blokovi);
}

struct ppm_data read_header_data(FILE* file)
{
    struct ppm_data rv;
    char buffer[1025] = { 0 };

    int header_data_read = 0;
    while(header_data_read != 3)
    {
        fgets(buffer, 1025, file);
        if(buffer[0] == '#') { continue; }

        switch(header_data_read)
        {
        case 0:
            sscanf(buffer, "%2c\n", &rv.file_type);
            rv.file_type[2] = '\0';
            break;
        case 1:
            sscanf(buffer, "%d %d\n", &rv.sirina, &rv.visina);
            break;
        case 2:
            sscanf(buffer, "%d\n", &rv.max_vrijednost);
            break;
        }
        ++header_data_read;
    }

    return rv;
}

struct ppm_data read_input_photo(char* filename)
{
    FILE* file = fopen(filename, "rb");
    struct ppm_data rv = read_header_data(file);
    int triplets = rv.sirina * rv.visina;
    rv.rgb_data = (struct int_triplet*) malloc(triplets * sizeof(struct int_triplet));

    for(int i = 0; i < triplets; ++i)
    {
        unsigned char buffer[3];
        fread(buffer, 3, sizeof(char), file);
        rv.rgb_data[i].prvi = buffer[0];
        rv.rgb_data[i].drugi = buffer[1];
        rv.rgb_data[i].treci = buffer[2];
    }

    fclose(file);

    return rv;
}

struct ycbcr_blok_data convert_rgb_to_ycbcr(struct ppm_data* rgb_data)
{
    int blokovi_per_row = rgb_data->sirina / 8;
    int length = rgb_data->sirina * rgb_data->visina;

    struct ycbcr_blok_data rv =
    {
        .sirina = rgb_data->sirina,
        .visina = rgb_data->visina,
        .blokovi = (struct double_blok*) malloc((rgb_data->sirina / 8) * (rgb_data->visina / 8) * sizeof(struct double_blok))
    };

    struct int_triplet* rgb = rgb_data->rgb_data;
    for(int i = 0; i < length; ++i, ++rgb)
    {
        int current_row = i / rgb_data->sirina;
        int current_column = i % rgb_data->sirina;
        int blok_row = current_row / 8;
        int blok_column = current_column / 8;
        int blok_index = blok_row * blokovi_per_row + blok_column;

        rv.blokovi[blok_index].prvi[current_row % 8][current_column % 8] = 0.299 * rgb->prvi + 0.587 * rgb->drugi + 0.114 * rgb->treci;
        rv.blokovi[blok_index].drugi[current_row % 8][current_column % 8] = -0.1687 * rgb->prvi - 0.3313 * rgb->drugi + 0.5 * rgb->treci + 128;
        rv.blokovi[blok_index].treci[current_row % 8][current_column % 8] = 0.5 * rgb->prvi - 0.4186 * rgb->drugi - 0.0813 * rgb->treci + 128;
    }

    return rv;
}

void shift_ycbcr(struct ycbcr_blok_data* ycbcr, int vrijednost)
{
    int blok_count = (ycbcr->sirina / 8) * (ycbcr->visina / 8);
    for(int b = 0; b < blok_count; ++b)
    {
        struct double_blok* blok= ycbcr->blokovi + b;
        for(int u = 0; u < 8; ++u)
        {
            for(int v = 0; v < 8; ++v)
            {
                blok->prvi[u][v] += vrijednost;
                blok->drugi[u][v] += vrijednost;
                blok->treci[u][v] += vrijednost;
            }
        }
    }
}

void discrete_cosine_transform(struct ycbcr_blok_data* ycbcr)
{
    int blok_count = (ycbcr->sirina / 8) * (ycbcr->visina / 8);
    for(int b = 0; b < blok_count; ++b)
    {
        struct double_blok* blok= ycbcr->blokovi + b;
        ippiDCT8x8Fwd_32f_C1I(blok->prvi);
        ippiDCT8x8Fwd_32f_C1I(blok->drugi);
        ippiDCT8x8Fwd_32f_C1I(blok->treci);
    }
}

void quantisation(struct ycbcr_blok_data* ycbcr)
{
    const float k1_table[8][8] =
    {
        { 16, 11, 10, 16, 24, 40, 51, 61 },
        { 12, 12, 14, 19, 26, 58, 60, 55 },
        { 14, 13, 16, 24, 40, 57, 69, 56 },
        { 14, 17, 22, 29, 51, 87, 80, 62 },
        { 18, 22, 37, 56, 68, 109, 103, 77 },
        { 24, 35, 55, 64, 81, 104, 113, 92 },
        { 49, 64, 78, 87, 103, 121, 120, 101 },
        { 72, 92, 95, 98, 112, 100, 103, 99 }
    };

    const float k2_table[8][8] =
    {
        { 17, 18, 24, 47, 99, 99, 99, 99 },
        { 18, 21, 26, 66, 99, 99, 99, 99 },
        { 24, 26, 56, 99, 99, 99, 99, 99 },
        { 47, 66, 99, 99, 99, 99, 99, 99 },
        { 99, 99, 99, 99, 99, 99, 99, 99 },
        { 99, 99, 99, 99, 99, 99, 99, 99 },
        { 99, 99, 99, 99, 99, 99, 99, 99 },
        { 99, 99, 99, 99, 99, 99, 99, 99 }
    };

    int blok_count = (ycbcr->sirina / 8) * (ycbcr->visina / 8);
    for(int b = 0; b < blok_count; ++b)
    {
        struct double_blok* blok= ycbcr->blokovi + b;
        for(int u = 0; u < 8; ++u)
        {
            for(int v = 0; v < 8; ++v)
            {
                blok->prvi[u][v] = round(blok->prvi[u][v] / k1_table[u][v]);
                blok->drugi[u][v] = round(blok->drugi[u][v] / k2_table[u][v]);
                blok->treci[u][v] = round(blok->treci[u][v] / k2_table[u][v]);
            }
        }
    }
}

struct ycbcr_blok_data encode(char* filename)
{
    struct ppm_data rgb = read_input_photo(filename);
    struct ycbcr_blok_data ycbcr = convert_rgb_to_ycbcr(&rgb);
    shift_ycbcr(&ycbcr, -128);
    discrete_cosine_transform(&ycbcr);
    quantisation(&ycbcr);

    free_ppm_data(&rgb);

    return ycbcr;
}

void write_to_file(struct ycbcr_blok_data* ycbcr, char* filename)
{
    FILE* file = fopen(filename, "w");
    fprintf(file, "%d %d\n\n", ycbcr->sirina, ycbcr->visina);

    int blok_count = (ycbcr->sirina / 8) * (ycbcr->visina / 8);
    for(int b = 0; b < blok_count; ++b)
    {
        struct double_blok* blok= ycbcr->blokovi + b;
        for(int i = 0; i < 64; i++)
        {
            fprintf(file, "%d ", (int)blok->prvi[zig_zag[i].row][zig_zag[i].coloumn]);
        }
    }
    fprintf(file, "\n\n");
    for(int b = 0; b < blok_count; ++b)
    {
        struct double_blok* blok= ycbcr->blokovi + b;
        for(int i = 0; i < 64; i++)
        {
            fprintf(file, "%d ", (int)blok->drugi[zig_zag[i].row][zig_zag[i].coloumn]);
        }
    }
    fprintf(file, "\n\n");
    for(int b = 0; b < blok_count; ++b)
    {
        struct double_blok* blok= ycbcr->blokovi + b;
        for(int i = 0; i < 64; i++)
        {
            fprintf(file, "%d ", (int)blok->treci[zig_zag[i].row][zig_zag[i].coloumn]);
        }
    }
    fprintf(file, "\n");
}
