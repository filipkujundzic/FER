#include <ctype.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define M_PI 3.14159265358979323846

struct
{
    int redak;
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

struct double_triplet
{
    double prvi;
    double drugi;
    double treci;
};

struct ppm_data
{
    char file_type[3];
    int sirina;
    int visina;
    int max_value;
    struct int_triplet* rgb_data;
};

void free_ppm_data(struct ppm_data* data_ptr);

struct double_blok
{
    struct double_triplet triplets[8][8];
};

struct ycbcr_blok_data
{
    int sirina;
    int visina;
    struct double_blok* bloks;
};

struct ycbcr_blok_data copy_ycbcr_blok_data(struct ycbcr_blok_data ycbcr);

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
    struct ycbcr_blok_data encod_data = encode(argv[1]);
    write_to_file(&encod_data, "out.txt");
    free_ycbcr_blok_data(&encod_data);
    return 0;
}

void free_ppm_data(struct ppm_data* data_ptr)
{
    free(data_ptr->rgb_data);
    data_ptr->rgb_data = NULL;
}

struct ycbcr_blok_data copy_ycbcr_blok_data(struct ycbcr_blok_data ycbcr)
{
    int blok_count = (ycbcr.sirina / 8) * (ycbcr.visina / 8);
    struct double_blok* old_bloks = ycbcr.bloks;
    ycbcr.bloks = (struct double_blok*) malloc(blok_count * sizeof(struct double_blok));
    memcpy(ycbcr.bloks, old_bloks, blok_count * sizeof(struct double_blok));
    return ycbcr;
}

void free_ycbcr_blok_data(struct ycbcr_blok_data* data_ptr)
{
    free(data_ptr->bloks);
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
            sscanf(buffer, "%d\n", &rv.max_value);
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
    int bloks_per_redak = rgb_data->sirina / 8;
    int length = rgb_data->sirina * rgb_data->visina;

    struct ycbcr_blok_data rv =
    {
        .sirina = rgb_data->sirina,
        .visina = rgb_data->visina,
        .bloks = (struct double_blok*) malloc((rgb_data->sirina / 8) * (rgb_data->visina / 8) * sizeof(struct double_blok))
    };

    struct int_triplet* rgb = rgb_data->rgb_data;
    for(int i = 0; i < length; ++i, ++rgb)
    {
        struct double_triplet triplet =
        {
            .prvi = 0.299 * rgb->prvi + 0.587 * rgb->drugi + 0.114 * rgb->treci,
            .drugi = -0.1687 * rgb->prvi - 0.3313 * rgb->drugi + 0.5 * rgb->treci + 128,
            .treci = 0.5 * rgb->prvi - 0.4186 * rgb->drugi - 0.0813 * rgb->treci + 128
        };

        int current_redak = i / rgb_data->sirina;
        int current_stupac = i % rgb_data->sirina;
        int blok_redak = current_redak / 8;
        int blok_stupac = current_stupac / 8;
        int blok_index = blok_redak * bloks_per_redak + blok_stupac;

        rv.bloks[blok_index].triplets[current_redak % 8][current_stupac % 8] = triplet;
    }

    return rv;
}

void shift_ycbcr(struct ycbcr_blok_data* ycbcr, int value)
{
    int blok_count = (ycbcr->sirina / 8) * (ycbcr->visina / 8);
    for(int b = 0; b < blok_count; ++b)
    {
        struct double_blok* blok = ycbcr->bloks + b;
        for(int u = 0; u < 8; ++u)
        {
            for(int v = 0; v < 8; ++v)
            {
                blok->triplets[u][v].prvi += value;
                blok->triplets[u][v].drugi += value;
                blok->triplets[u][v].treci += value;
            }
        }
    }
}

void discrete_cosine_transform(struct ycbcr_blok_data* ycbcr)
{

    struct ycbcr_blok_data copy = copy_ycbcr_blok_data(*ycbcr);
    int blok_count = (ycbcr->sirina / 8) * (ycbcr->visina / 8);
    for(int b = 0; b < blok_count; ++b)
    {
        struct double_blok* blok = ycbcr->bloks + b;
        struct double_blok* originalni_blok = copy.bloks + b;
        for(int u = 0; u < 8; ++u)
        {
            for(int v = 0; v < 8; ++v)
            {
                double cu = (u == 0 ? 1 / sqrt(2) : 1);
                double cv = (v == 0 ? 1 / sqrt(2) : 1);

                double sum_y = 0;
                double sum_cb = 0;
                double sum_cr = 0;
                for(int i = 0; i < 8; ++i)
                {
                    for(int j = 0; j < 8; ++j)
                    {
                        double factor = cos((2 * i + 1) * u * M_PI / 16.0) * cos((2 * j + 1) * v * M_PI / 16.0);
                        sum_y += originalni_blok->triplets[i][j].prvi * factor;
                        sum_cb += originalni_blok->triplets[i][j].drugi * factor;
                        sum_cr += originalni_blok->triplets[i][j].treci * factor;
                    }
                }

                blok->triplets[u][v].prvi = 0.25 * cv * cu * sum_y;
                blok->triplets[u][v].drugi = 0.25 * cv * cu * sum_cb;
                blok->triplets[u][v].treci = 0.25 * cv * cu * sum_cr;
            }
        }
    }
    free_ycbcr_blok_data(&copy);
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
        struct double_blok* blok = ycbcr->bloks + b;
        for(int u = 0; u < 8; ++u)
        {
            for(int v = 0; v < 8; ++v)
            {
                blok->triplets[u][v].prvi = round(blok->triplets[u][v].prvi / k1_table[u][v]);
                blok->triplets[u][v].drugi = round(blok->triplets[u][v].drugi / k2_table[u][v]);
                blok->triplets[u][v].treci = round(blok->triplets[u][v].treci / k2_table[u][v]);
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
        struct double_blok* blok = ycbcr->bloks + b;
        for(int i = 0; i < 64; i++)
        {
            fprintf(file, "%d ", (int)blok->triplets[zig_zag[i].redak][zig_zag[i].coloumn].prvi);
        }
    }
    fprintf(file, "\n\n");
    for(int b = 0; b < blok_count; ++b)
    {
        struct double_blok* blok = ycbcr->bloks + b;
        for(int i = 0; i < 64; i++)
        {
            fprintf(file, "%d ", (int)blok->triplets[zig_zag[i].redak][zig_zag[i].coloumn].drugi);
        }
    }
    fprintf(file, "\n\n");
    for(int b = 0; b < blok_count; ++b)
    {
        struct double_blok* blok = ycbcr->bloks + b;
        for(int i = 0; i < 64; i++)
        {
            fprintf(file, "%d ", (int)blok->triplets[zig_zag[i].redak][zig_zag[i].coloumn].treci);
        }
    }
    fprintf(file, "\n");
}
