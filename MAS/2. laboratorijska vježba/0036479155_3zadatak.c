#include <ctype.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define BUFFER_SIZE 32
#define HEADER_LINES 4
#define GROUPS 16

#define FILE_NOT_FOUND "File %s not found!"
#define HEADER_ERROR "Expected a 4 line pgm header, but reached EOF at line %d"

char* l_trim(char *s) {
    while(isspace(*s)) {
        s++;
    }

    return s;
}

char* r_trim(char *s) {
    char* back = s + strlen(s);
    while(isspace(*--back));

    *(back+1) = '\0';
    return s;
}

char* trim(char *s) {
    return r_trim(l_trim(s));
}


struct PictureData_s {
    uint8_t** data;
    long long width;
    long long height;
} PictureData_default = {NULL, 0, 0};

typedef struct PictureData_s PictureData;

PictureData* read_pic_data(const char* image_path) {
    if(image_path == NULL) {
        image_path = "lenna.pgm";
    }


    FILE *fp = fopen(image_path, "r");

    if(fp == NULL) {
        fprintf(stderr, FILE_NOT_FOUND, image_path);
        exit(-1);
    }


    char buffer[BUFFER_SIZE];
    char results[HEADER_LINES][BUFFER_SIZE];
    char *t_ptr;


    for(int i = 0; i < HEADER_LINES; ++i) {
        if (!fgets(buffer, sizeof(buffer), fp)) {
            fprintf(stderr, HEADER_ERROR, i + 1);
            exit(-1);
        }

        strcpy(results[i], trim(buffer));
    }


    PictureData* to_return = (PictureData*)malloc(sizeof(PictureData));
    to_return->width = strtoll(results[1], &t_ptr, 10);
    to_return->height = strtoll(results[2], &t_ptr, 10);


    to_return->data = (uint8_t**)malloc(to_return->height * sizeof(uint8_t*));
    for(uint64_t i = 0; i < to_return->height; ++i) {
        to_return->data[i] = (uint8_t*)malloc(to_return->width * sizeof(uint8_t));
    }


    uint8_t row_buffer[to_return->width];

    for(uint64_t i = 0; fread(row_buffer, 1, to_return->width, fp); ++i) {
        for(uint64_t j = 0; j < to_return->width; ++j) {
            to_return->data[i][j] = row_buffer[j];
        }
    }

    return to_return;
}

void free_pic_data(PictureData* pic_data_ptr) {
    for(uint64_t i = 0; i < pic_data_ptr->height; ++i) {
        free(pic_data_ptr->data[i]);
    }

    free(pic_data_ptr->data);
}


uint8_t get_group(uint8_t byte) {
    int x;
    x = pow(2,4);
    return byte / x;
}

uint64_t* get_group_statistics(PictureData image_data) {
    uint64_t* group_statistics = (uint64_t*)malloc(GROUPS * sizeof(uint64_t));

    for(uint64_t i = 0; i < GROUPS; ++i) {
        group_statistics[i] = 0;
    }

    for(uint64_t i = 0; i < image_data.height; ++i) {
        for(uint64_t j = 0; j < image_data.width; ++j) {
            ++group_statistics[get_group(image_data.data[i][j]) % GROUPS];
        }
    }

    return group_statistics;
}

void free_group_statistics(uint64_t* group_statistics) {
    free(group_statistics);
}


int main(int argc, char* argv[]) {
    char* image_path = NULL;
    if(argc < 2){
        char* image_path = NULL;
    }
    else{
        char* image_path = argv[1];
    }

    PictureData* img = read_pic_data(image_path);
    uint64_t* group_statistics = get_group_statistics(*img);

    uint64_t n_total = 0;

    for(uint64_t i = 0; i < GROUPS; ++i) {
        n_total += group_statistics[i];
    }

    for(uint64_t i = 0; i < GROUPS; ++i) {
        printf("%lu %f\n", i, (double)group_statistics[i] / n_total);
    }

    free_pic_data(img);
    free_group_statistics(group_statistics);

    return 0;
}
