#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include "ext2.h"


// Pointer to the beginning of the disk (byte 0)
static const unsigned char *disk = NULL;

// helper to see if the inode is in use
int is_inode_in_use(unsigned char *inode_bitmap, int inode_index) {
    int byte = inode_index / 8;  // find the byte containing the bit
    int bit = inode_index % 8;  // find the bit within the byte
    return (inode_bitmap[byte] >> bit) & 1;
}

int main(int argc, char *argv[])
{
	if (argc != 2) {
		fprintf(stderr, "Usage: %s <image file name>\n", argv[0]);
		exit(1);
	}
	int fd = open(argv[1], O_RDONLY);
	if (fd == -1) {
		perror("open");
		exit(1);
	}

	// Map the disk image into memory so that we don't have to do any explicit reads
	disk = mmap(NULL, 128 * EXT2_BLOCK_SIZE, PROT_READ, MAP_SHARED, fd, 0);
	if (disk == MAP_FAILED) {
		perror("mmap");
		exit(1);
	}

	const struct ext2_super_block *sb = (const struct ext2_super_block*)(disk + EXT2_BLOCK_SIZE);
	printf("Inodes: %d\n", sb->s_inodes_count);
	printf("Blocks: %d\n", sb->s_blocks_count);

    // task 1
    // access the block group descriptor
    const struct ext2_group_desc *bg = (const struct ext2_group_desc *)(disk + EXT2_BLOCK_SIZE * 2);
    printf("Block group:\n");
    printf("    block bitmap: %d\n", bg->bg_block_bitmap);
    printf("    inode bitmap: %d\n", bg->bg_inode_bitmap);
    printf("    inode table: %d\n", bg->bg_inode_table);
    printf("    free blocks: %d\n", bg->bg_free_blocks_count);
    printf("    free inodes: %d\n", bg->bg_free_inodes_count);
    printf("    used_dirs: %d\n", bg->bg_used_dirs_count);

    // task 2
    printf("Block bitmap: ");
    unsigned char *block_bitmap = (unsigned char *)(disk + EXT2_BLOCK_SIZE * bg->bg_block_bitmap);
    for (int i = 0; i < sb->s_blocks_count / 8; i++) {
        for (int bit = 0; bit < 8; bit++) {
           printf("%d", (block_bitmap[i] >> bit) & 1);
        }
        printf(" ");
    }
    printf("\n");

    printf("Inode bitmap: ");
    unsigned char *inode_bitmap = (unsigned char *)(disk + EXT2_BLOCK_SIZE * bg->bg_inode_bitmap);
    for (int i = 0; i < sb->s_inodes_count / 8; i++) {
        for (int bit = 0; bit < 8; bit++) {
            printf("%d", (inode_bitmap[i] >> bit) & 1);
        }
        printf(" ");
    }
    printf("\n");


    // task 3
    printf("\nInodes:\n");
    // access inode table
    const struct ext2_inode *inode_table = (const struct ext2_inode *)(disk + EXT2_BLOCK_SIZE * bg->bg_inode_table);

    // print the root inode (inode number 2)
    if (is_inode_in_use(inode_bitmap, 2 - 1)) {
        const struct ext2_inode *root_inode = &inode_table[2 - 1]; // index 1 corresponds to inode 2
        int blocks = root_inode->i_blocks;

        printf("[2] type: %c size: %d links: %d blocks: %d\n",
               (root_inode->i_mode & EXT2_S_IFDIR) ? 'd' : 'f',
               root_inode->i_size,
               root_inode->i_links_count,
               blocks);

        printf("[2] Blocks: ");
        for (int j = 0; j < 15 && root_inode->i_block[j]; j++) {
            printf("%d ", root_inode->i_block[j]);
        }
        printf("\n");
    }

    // iterate over inodes starting at index 11 (inode number 12)
    for (int i = 11; i < sb->s_inodes_count; i++) {
        if (is_inode_in_use(inode_bitmap, i)) {
            const struct ext2_inode *inode = &inode_table[i];
            printf("[%d] type: %c size: %d links: %d blocks: %d\n",
                   i + 1, // convert zero-based index to one-based inode number
                   (inode->i_mode & EXT2_S_IFDIR) ? 'd' : 'f',
                   inode->i_size,
                   inode->i_links_count,
                   inode->i_blocks);
            printf("[%d] Blocks: ", i + 1);
            for (int j = 0; j < 15 && inode->i_block[j]; j++) {
                printf("%d ", inode->i_block[j]);
            }
            printf("\n");
        }
    }

	return 0;
}
