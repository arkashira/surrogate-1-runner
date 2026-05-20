/*
 * PCI Express 5.0 driver stub
 *
 * This file implements minimal support for PCIe 5.0 configuration
 * required by the surrogate-1 project. It exposes a simple API
 * to initialize the PCIe bus, configure the number of GPUs, and
 * expose the bandwidth characteristics.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Constants */
#define PCIe_LINK_SPEED_GBPS   5.0
#define PCIe_LINK_WIDTH        16
#define PCIe_MAX_BANDWIDTH_GBPS (PCIe_LINK_SPEED_GBPS * PCIe_LINK_WIDTH)

/* Forward declaration of NVLink init (defined in nvlink.c) */
extern int init_nvlink(int gpu_count);

/* Structure representing a PCIe device (GPU) */
typedef struct {
    int id;                     /* GPU identifier */
    double link_speed_gbps;     /* Link speed in GB/s */
    int link_width;             /* Number of lanes */
    double bandwidth_gbps;      /* Effective bandwidth */
} pcie_device_t;

/* Global array of GPUs */
static pcie_device_t *gpus = NULL;
static int gpu_count = 0;

/* Initialize PCIe 5.0 bus and configure GPUs */
int init_pcie5(int count)
{
    if (count <= 0 || count > 4) {
        fprintf(stderr, "PCIe5 init: GPU count must be between 1 and 4\n");
        return -1;
    }

    /* Allocate GPU array */
    gpus = calloc(count, sizeof(pcie_device_t));
    if (!gpus) {
        perror("PCIe5 init: calloc");
        return -1;
    }

    /* Configure each GPU */
    for (int i = 0; i < count; ++i) {
        gpus[i].id = i;
        gpus[i].link_speed_gbps = PCIe_LINK_SPEED_GBPS;
        gpus[i].link_width = PCIe_LINK_WIDTH;
        gpus[i].bandwidth_gbps = PCIe_MAX_BANDWIDTH_GBPS;
    }

    gpu_count = count;

    /* Initialize NVLink interconnect between GPUs */
    if (init_nvlink(count) != 0) {
        fprintf(stderr, "PCIe5 init: NVLink initialization failed\n");
        free(gpus);
        gpus = NULL;
        return -1;
    }

    printf("PCIe5 init: Configured %d GPUs with %0.1f GB/s link speed, %d lanes, "
           "%0.1f GB/s bandwidth each\n",
           gpu_count, PCIe_LINK_SPEED_GBPS, PCIe_LINK_WIDTH,
           PCIe_MAX_BANDWIDTH_GBPS);

    return 0;
}

/* Retrieve GPU info by index */
const pcie_device_t *get_gpu_info(int index)
{
    if (!gpus || index < 0 || index >= gpu_count) {
        return NULL;
    }
    return &gpus[index];
}

/* Clean up PCIe resources */
void cleanup_pcie5(void)
{
    if (gpus) {
        free(gpus);
        gpus = NULL;
    }
    gpu_count = 0;
}