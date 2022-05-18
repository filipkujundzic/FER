#include <ctype.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 32
#define N_HEADER_LINES 4
#define BLOCK_WIDTH 16
#define BLOCK_HEIGHT 16
#define BLOCK_X_PLUS_DIFF 16
#define BLOCK_X_MINUS_DIFF 16
#define BLOCK_Y_PLUS_DIFF 16
#define BLOCK_Y_MINUS_DIFF 16

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
    int64_t width;
    int64_t height;
} PictureData_default = {NULL, 0, 0};

typedef struct PictureData_s PictureData;

struct BlockData_s {
    double** data;
    int64_t width;
    int64_t height;
    uint64_t center_x;
    uint64_t center_y;
} BlockData_default = {NULL, 0, 0, 0, 0};

typedef struct BlockData_s BlockData;

PictureData* read_pic_data(const char* image_path) {
    FILE *fp = fopen(image_path, "r");

    if(fp == NULL) {
        fprintf(stderr, FILE_NOT_FOUND, image_path);
        exit(-1);
    }

    char buffer[BUFFER_SIZE];
    char results[N_HEADER_LINES][BUFFER_SIZE];
    char *t_ptr;

    for(int i = 0; i < N_HEADER_LINES; ++i) {
        if (!fgets(buffer, sizeof(buffer), fp)) {
            fprintf(stderr, HEADER_ERROR, i + 1);
            exit(-1);
        }

        strcpy(results[i], trim(buffer));
    }

    PictureData* return_data = (PictureData*)malloc(sizeof(PictureData));
    return_data->width = strtoll(results[1], &t_ptr, 10);
    return_data->height = strtoll(results[2], &t_ptr, 10);

    return_data->data = (uint8_t**)malloc(return_data->height * sizeof(uint8_t*));
    for(uint64_t i = 0; i < return_data->height; ++i) {
        return_data->data[i] = (uint8_t*)malloc(return_data->width * sizeof(uint8_t));
    }

    uint8_t row_buffer[return_data->width];

    for(uint64_t i = 0; fread(row_buffer, 1, return_data->width, fp); ++i) {
        for(uint64_t j = 0; j < return_data->width; ++j) {
            return_data->data[i][j] = row_buffer[j];
        }
    }

    return return_data;
}

void free_image_data(PictureData* image_data_ptr) {
    for(uint64_t i = 0; i < image_data_ptr->height; ++i) {
        free(image_data_ptr->data[i]);
    }

    free(image_data_ptr->data);
}

void free_block_data(BlockData* block_data_ptr) {
    for(uint64_t i = 0; i < block_data_ptr->height; ++i) {
        free(block_data_ptr->data[i]);
    }

    free(block_data_ptr->data);
}

struct Vector2D_i64_s {
    int64_t x;
    int64_t y;
} Vector2D_i64_default = {0, 0};

typedef struct Vector2D_i64_s Vector2D_i64;

void free_vector2d_i64(Vector2D_i64* vector) {
    free(vector);
}

PictureData* get_block_from_origin(PictureData image, int64_t origin_x, int64_t origin_y) {
    PictureData* return_data = (PictureData*)malloc(sizeof(PictureData));
    return_data->width = BLOCK_WIDTH;
    return_data->height = BLOCK_HEIGHT;

    return_data->data = (uint8_t**)malloc(return_data->height * sizeof(uint8_t*));
    for(uint64_t i = 0; i < return_data->height; ++i) {
        return_data->data[i] = (uint8_t*)malloc(return_data->width * sizeof(uint8_t));

        for(uint64_t j = 0; j < return_data->width; ++j) {
            return_data->data[i][j] = image.data[origin_y + i][origin_x + j];
        }
    }

    return return_data;
}

double get_mad_of_block(PictureData reference_block, PictureData interesting_block) {
    uint64_t width_max = reference_block.width;
    uint64_t height_max = reference_block.height;

    if(interesting_block.width < width_max) {
        width_max = interesting_block.width;
    }

    if(interesting_block.height < height_max) {
        height_max = interesting_block.height;
    }

    double result = 0;

    for(uint64_t i = 0; i < height_max; ++i) {
        for(uint64_t j = 0; j < width_max; ++j) {
            if(reference_block.data[i][j] > interesting_block.data[i][j]) {
                result += reference_block.data[i][j] - interesting_block.data[i][j];
            } else {
                result += interesting_block.data[i][j] - reference_block.data[i][j];
            }
        }
    }

    double n_elements = (double)width_max * height_max;

    return result / n_elements;
}

BlockData* get_block_diff(PictureData reference_image, PictureData interesting_image, uint64_t origin_block_index) {

    uint64_t blocks_per_row = interesting_image.width / BLOCK_WIDTH;
    int64_t origin_x = (origin_block_index % blocks_per_row) * BLOCK_WIDTH;
    int64_t origin_y = (origin_block_index / blocks_per_row) * BLOCK_HEIGHT;

    PictureData* reference_block = get_block_from_origin(interesting_image, origin_x, origin_y);

    int64_t left_offset = BLOCK_X_MINUS_DIFF;
    int64_t right_offset = BLOCK_X_PLUS_DIFF;
    int64_t up_offset = BLOCK_Y_MINUS_DIFF;
    int64_t down_offset = BLOCK_Y_PLUS_DIFF;

    if(origin_x < left_offset) {
        left_offset = origin_x;
    }

    if(origin_y < down_offset) {
        up_offset = origin_y;
    }

    if(origin_x + BLOCK_WIDTH + right_offset >= interesting_image.width) {
        right_offset = interesting_image.width - BLOCK_WIDTH - origin_x;
    }

    if(origin_y + BLOCK_HEIGHT + down_offset >= interesting_image.height) {
        down_offset = interesting_image.height - BLOCK_HEIGHT - origin_y;
    }

    uint64_t x_start = origin_x - left_offset;
    uint64_t y_start = origin_y - up_offset;

    BlockData* return_data = (BlockData*)malloc(sizeof(BlockData));
    return_data->width = left_offset + right_offset + 1;
    return_data->height = down_offset + up_offset + 1;
    return_data->center_x = left_offset;
    return_data->center_y = up_offset;

    return_data->data = (double**)malloc(return_data->height * sizeof(double*));
    for(uint64_t i = 0; i < return_data->height; ++i) {
        return_data->data[i] = (double*)malloc(return_data->width * sizeof(double));
    }

    for(uint64_t i = 0; i < return_data->height; ++i) {
        for(uint64_t j = 0; j < return_data->width; ++j) {
            int64_t current_origin_x = x_start + j;
            int64_t current_origin_y = y_start + i;

            PictureData* t_block = get_block_from_origin(reference_image, current_origin_x, current_origin_y);

            return_data->data[i][j] = get_mad_of_block(*reference_block, *t_block);

            free_image_data(t_block);
        }
    }

    free_image_data(reference_block);

    return return_data;
}


Vector2D_i64* get_mov_vect(BlockData block_difference) {
    Vector2D_i64* best = (Vector2D_i64*)malloc(sizeof(Vector2D_i64));
    best->x = 0;
    best->y = 0;

    for(uint64_t i = 0; i < block_difference.height; ++i) {
        for(uint64_t j = 0; j < block_difference.width; ++j) {
            if(block_difference.data[i][j] < block_difference.data[best->y][best->x]) {
                best->x = j;
                best->y = i;
            }
        }
    }

    best->x -=  block_difference.center_x;
    best->y -=  block_difference.center_y;

    return best;
}


int main(int argc, char* argv[]) {
    uint64_t block_index = 0;
    char* ref_image_path = NULL;
    char* interesting_image_path = NULL;

    char* t_ptr;

    if(argc > 1) {
        block_index = strtoll(argv[1], &t_ptr, 10);

        if(argc > 2) {
            ref_image_path = argv[2];

            if(argc > 3) {
                interesting_image_path = argv[3];
            }
        }
    }

    if(ref_image_path == NULL) {
        ref_image_path = "lenna.pgm";
    }

    if(interesting_image_path == NULL) {
        interesting_image_path = "lenna1.pgm";
    }

    PictureData* reference_img = read_pic_data(ref_image_path);
    PictureData* interesting_img = read_pic_data(interesting_image_path);

    BlockData* block_difference = get_block_diff(*reference_img, *interesting_img, block_index);
    Vector2D_i64* movement_vector = get_mov_vect(*block_difference);

    printf("%ld,%ld\n", movement_vector->x, movement_vector->y);

    free_vector2d_i64(movement_vector);
    free_block_data(block_difference);

    free_image_data(interesting_img);
    free_image_data(reference_img);

    return 0;
}
