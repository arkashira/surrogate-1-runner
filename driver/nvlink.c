/*
 * NVLink driver stub
 *
 * Provides minimal NVLink interconnect support between GPUs.
 * For each pair of GPUs, an NVLink channel is created with
 * a bandwidth of 32 GB/s (PCIe 5.0 theoretical maximum).
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* NVLink bandwidth per link in GB/s */
#define NVLINK_BANDWIDTH_GBPS 32.0

/* Structure representing an NVLink channel between two GPUs */
typedef struct {
    int src_gpu;                /* Source GPU index */
    int dst_gpu;                /* Destination GPU index */
    double bandwidth_gbps;      /* Bandwidth of this link */
} nvlink_link_t;

/* Global array of NVLink links */
static nvlink_link_t *nvlinks = NULL;
static int nvlink_count = 0;

/* Initialize NVLink interconnect for a given number of GPUs */
int init_nvlink(int gpu_count)
{
    if (gpu_count <= 0) {
        fprintf(stderr, "NVLink init: GPU count must be positive\n");
        return -1;
    }

    /* Number of links in a full mesh: n*(n-1)/2 */
    nvlink_count = gpu_count * (gpu_count - 1) / 2;
    nvlinks = calloc(nvlink_count, sizeof(nvlink_link_t));
    if (!nvlinks) {
        perror("NVLink init: calloc");
        return -1;
    }

    int idx = 0;
    for (int i = 0; i < gpu_count; ++i) {
        for (int j = i + 1; j < gpu_count; ++j) {
            nvlinks[idx].src_gpu = i;
            nvlinks[idx].dst_gpu = j;
            nvlinks[idx].bandwidth_gbps = NVLINK_BANDWIDTH_GBPS;
            ++idx;
        }
    }

    printf("NVLink init: Created %d links between %d GPUs, each with %0.1f GB/s\n",
           nvlink_count, gpu_count, NVLINK_BANDWIDTH_GBPS);

    return 0;
}

/* Retrieve NVLink link info by index */
const nvlink_link_t *get_nvlink_info(int index)
{
    if (!nvlinks || index < 0 || index >= nvlink_count) {
        return NULL;
    }
    return &nvlinks[index];
}

/* Clean up NVLink resources */
void cleanup_nvlink(void)
{
    if (nvlinks) {
        free(nvlinks);
        nvlinks = NULL;
    }
    nvlink_count = 0;
}