/**
 * 01/11/2021
 * Módulo: constants
 * -----------------
 * Autores:
 * - Daniel Mohedano    <daniel.mohedano@estudiante.uam.es>
 * - Silvia Sopeña      <silvia.sopenna@estudiante.uam.es>
 * -----------------------------------------------------------
 * Este módulo alberga las constantes necesarias para la ejecución de los programas.
 */
#ifndef CONSTANTS_H
#define CONSTANTS_H
#include <stdint.h>

/* Constantes para los programas */
#define LANG_SIZE 26
#define N_CLAVES_AFIN 312

static const unsigned short AFIN_CLAVES[N_CLAVES_AFIN][2] = {
	{ 1, 0}, { 1, 1}, { 1, 2}, { 1, 3}, { 1, 4}, { 1, 5}, { 1, 6}, { 1, 7}, { 1, 8}, { 1, 9}, { 1, 10}, { 1, 11}, { 1, 12}, { 1, 13}, { 1, 14}, { 1, 15}, { 1, 16}, { 1, 17}, { 1, 18}, { 1, 19}, { 1, 20}, { 1, 21}, { 1, 22}, { 1, 23}, { 1, 24}, { 1, 25}, 
	{ 3, 0}, { 3, 1}, { 3, 2}, { 3, 3}, { 3, 4}, { 3, 5}, { 3, 6}, { 3, 7}, { 3, 8}, { 3, 9}, { 3, 10}, { 3, 11}, { 3, 12}, { 3, 13}, { 3, 14}, { 3, 15}, { 3, 16}, { 3, 17}, { 3, 18}, { 3, 19}, { 3, 20}, { 3, 21}, { 3, 22}, { 3, 23}, { 3, 24}, { 3, 25}, 
	{ 5, 0}, { 5, 1}, { 5, 2}, { 5, 3}, { 5, 4}, { 5, 5}, { 5, 6}, { 5, 7}, { 5, 8}, { 5, 9}, { 5, 10}, { 5, 11}, { 5, 12}, { 5, 13}, { 5, 14}, { 5, 15}, { 5, 16}, { 5, 17}, { 5, 18}, { 5, 19}, { 5, 20}, { 5, 21}, { 5, 22}, { 5, 23}, { 5, 24}, { 5, 25}, 
	{ 7, 0}, { 7, 1}, { 7, 2}, { 7, 3}, { 7, 4}, { 7, 5}, { 7, 6}, { 7, 7}, { 7, 8}, { 7, 9}, { 7, 10}, { 7, 11}, { 7, 12}, { 7, 13}, { 7, 14}, { 7, 15}, { 7, 16}, { 7, 17}, { 7, 18}, { 7, 19}, { 7, 20}, { 7, 21}, { 7, 22}, { 7, 23}, { 7, 24}, { 7, 25}, 
	{ 9, 0}, { 9, 1}, { 9, 2}, { 9, 3}, { 9, 4}, { 9, 5}, { 9, 6}, { 9, 7}, { 9, 8}, { 9, 9}, { 9, 10}, { 9, 11}, { 9, 12}, { 9, 13}, { 9, 14}, { 9, 15}, { 9, 16}, { 9, 17}, { 9, 18}, { 9, 19}, { 9, 20}, { 9, 21}, { 9, 22}, { 9, 23}, { 9, 24}, { 9, 25}, 
	{ 11, 0}, { 11, 1}, { 11, 2}, { 11, 3}, { 11, 4}, { 11, 5}, { 11, 6}, { 11, 7}, { 11, 8}, { 11, 9}, { 11, 10}, { 11, 11}, { 11, 12}, { 11, 13}, { 11, 14}, { 11, 15}, { 11, 16}, { 11, 17}, { 11, 18}, { 11, 19}, { 11, 20}, { 11, 21}, { 11, 22}, { 11, 23}, { 11, 24}, { 11, 25}, 
	{ 15, 0}, { 15, 1}, { 15, 2}, { 15, 3}, { 15, 4}, { 15, 5}, { 15, 6}, { 15, 7}, { 15, 8}, { 15, 9}, { 15, 10}, { 15, 11}, { 15, 12}, { 15, 13}, { 15, 14}, { 15, 15}, { 15, 16}, { 15, 17}, { 15, 18}, { 15, 19}, { 15, 20}, { 15, 21}, { 15, 22}, { 15, 23}, { 15, 24}, { 15, 25}, 
	{ 17, 0}, { 17, 1}, { 17, 2}, { 17, 3}, { 17, 4}, { 17, 5}, { 17, 6}, { 17, 7}, { 17, 8}, { 17, 9}, { 17, 10}, { 17, 11}, { 17, 12}, { 17, 13}, { 17, 14}, { 17, 15}, { 17, 16}, { 17, 17}, { 17, 18}, { 17, 19}, { 17, 20}, { 17, 21}, { 17, 22}, { 17, 23}, { 17, 24}, { 17, 25}, 
	{ 19, 0}, { 19, 1}, { 19, 2}, { 19, 3}, { 19, 4}, { 19, 5}, { 19, 6}, { 19, 7}, { 19, 8}, { 19, 9}, { 19, 10}, { 19, 11}, { 19, 12}, { 19, 13}, { 19, 14}, { 19, 15}, { 19, 16}, { 19, 17}, { 19, 18}, { 19, 19}, { 19, 20}, { 19, 21}, { 19, 22}, { 19, 23}, { 19, 24}, { 19, 25}, 
	{ 21, 0}, { 21, 1}, { 21, 2}, { 21, 3}, { 21, 4}, { 21, 5}, { 21, 6}, { 21, 7}, { 21, 8}, { 21, 9}, { 21, 10}, { 21, 11}, { 21, 12}, { 21, 13}, { 21, 14}, { 21, 15}, { 21, 16}, { 21, 17}, { 21, 18}, { 21, 19}, { 21, 20}, { 21, 21}, { 21, 22}, { 21, 23}, { 21, 24}, { 21, 25}, 
	{ 23, 0}, { 23, 1}, { 23, 2}, { 23, 3}, { 23, 4}, { 23, 5}, { 23, 6}, { 23, 7}, { 23, 8}, { 23, 9}, { 23, 10}, { 23, 11}, { 23, 12}, { 23, 13}, { 23, 14}, { 23, 15}, { 23, 16}, { 23, 17}, { 23, 18}, { 23, 19}, { 23, 20}, { 23, 21}, { 23, 22}, { 23, 23}, { 23, 24}, { 23, 25}, 
	{ 25, 0}, { 25, 1}, { 25, 2}, { 25, 3}, { 25, 4}, { 25, 5}, { 25, 6}, { 25, 7}, { 25, 8}, { 25, 9}, { 25, 10}, { 25, 11}, { 25, 12}, { 25, 13}, { 25, 14}, { 25, 15}, { 25, 16}, { 25, 17}, { 25, 18}, { 25, 19}, { 25, 20}, { 25, 21}, { 25, 22}, { 25, 23}, { 25, 24}, { 25, 25}, 
};

/* Constantes para el DES */
#define BITS_IN_PC1 56
#define BITS_IN_PC2 48
#define ROUNDS 16
#define BITS_IN_IP 64
#define BITS_IN_E 48
#define BITS_IN_P 32
#define NUM_S_BOXES 8
#define ROWS_PER_SBOX 4
#define COLUMNS_PER_SBOX 16
#define BITS_IN_DES 64

#define FIRST_BIT   0x8000000000000000 // 1000.......0000 en 64b
#define LEFT_KEY    0xFFFFFFF000000000
#define RIGHT_KEY   0x0000000FFFFFFF00
#define LEFT_BLOCK  0xFFFFFFFF00000000
#define RIGHT_BLOCK 0x00000000FFFFFFFF
#define MASK_6_BIT  0xFC00000000000000
#define MASK_4_BIT  0xF000000000000000

/* "permutaci�n" PC1 */
static const unsigned short PC1[BITS_IN_PC1] = { 
	57, 49, 41, 33, 25, 17, 9,
	1, 58, 50, 42, 34, 26, 18,
	10, 2, 59, 51, 43, 35, 27,
	19, 11, 3, 60, 52, 44, 36,
	63, 55, 47, 39, 31, 23, 15,
	7, 62, 54, 46, 38, 30, 22,
	14, 6, 61, 53, 45, 37, 29,
	21, 13, 5, 28, 20, 12, 4
};

/* "permutaci�n" PC2 */
static const unsigned short PC2[BITS_IN_PC2] = {
	14, 17, 11, 24, 1, 5,
	3, 28, 15, 6, 21, 10,
	23, 19, 12, 4, 26, 8,
	16, 7, 27, 20, 13, 2,
	41, 52, 31, 37, 47, 55,
	30, 40, 51, 45, 33, 48,
	44, 49, 39, 56, 34, 53,
	46, 42, 50, 36, 29, 32
};

/* n�mero de bits que hay que rotar cada semiclave seg�n el n�mero de ronda */
static const unsigned short ROUND_SHIFTS[ROUNDS] = {
	1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
};

/* permutaci�n IP */
static const unsigned short IP[BITS_IN_IP] = {
	58, 50, 42, 34, 26, 18, 10, 2,
	60, 52, 44, 36, 28, 20, 12, 4,
	62, 54, 46, 38, 30, 22, 14, 6,
	64, 56, 48, 40, 32, 24, 16, 8,
	57, 49, 41, 33, 25, 17, 9, 1,
	59, 51, 43, 35, 27, 19, 11, 3,
	61, 53, 45, 37, 29, 21, 13, 5,
	63, 55, 47, 39, 31, 23, 15, 7
};

/* inversa de IP */
static const unsigned short IP_INV[BITS_IN_IP] = {
	40, 8, 48, 16, 56, 24, 64, 32,
	39, 7, 47, 15, 55, 23, 63, 31,
	38, 6, 46, 14, 54, 22, 62, 30,
	37, 5, 45, 13, 53, 21, 61, 29,
	36, 4, 44, 12, 52, 20, 60, 28,
	35, 3, 43, 11, 51, 19, 59, 27,
	34, 2, 42, 10, 50, 18, 58, 26,
	33, 1, 41, 9, 49, 17, 57, 25
};

/* expansi�n E */
static const unsigned short E[BITS_IN_E] = {
	32, 1, 2, 3, 4, 5,
	4, 5, 6, 7, 8, 9,
	8, 9, 10, 11, 12, 13,
	12, 13, 14, 15, 16, 17,
	16, 17, 18, 19, 20, 21,
	20, 21, 22, 23, 24, 25,
	24, 25, 26, 27, 28, 29,
	28, 29, 30, 31, 32, 1
};

/* permutaci�n P */
static const unsigned short P[BITS_IN_P] = {
	16, 7, 20, 21,
	29, 12, 28, 17,
	1, 15, 23, 26,
	5, 18, 31, 10,
	2, 8, 24, 14,
	32, 27, 3, 9,
	19, 13, 30, 6,
	22, 11, 4, 25
};

/* cajas S */
static const unsigned short S_BOXES[NUM_S_BOXES][ROWS_PER_SBOX][COLUMNS_PER_SBOX] = {
	{	{ 14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7 },
		{ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8 },
		{ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0 },
		{ 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 } 	},
	{
		{ 15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10 },
		{ 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5 },
		{ 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15 },
		{ 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 }	},

	{	{ 10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8 },
		{ 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1 },
		{ 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7 },
		{ 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 }	},

	{	{ 7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15 },
		{ 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9 },
		{ 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4 },
		{ 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14 }	},
	{
		{ 2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9 },
		{ 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6 },
		{ 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14 },
		{ 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 }	},
	{	
		{ 12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11 },
		{ 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8 },
		{ 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6 },
		{ 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13 }	},
	{
 		{ 4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1 },
		{ 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6 },
		{ 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2 },
		{ 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12 }	},
	{
		{ 13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7 },
		{ 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2 },
		{ 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8 },
		{ 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11 }	}
};

/* Constantes para el AES con clave de 128 bits */
#define BYTES_PER_WORD 4
#define ROWS_PER_SBOX_AES 16
#define COLUMNS_PER_SBOX_AES 16
#define HEX_STRING_SIZE 3

static const char DIRECT_SBOX[ROWS_PER_SBOX_AES][COLUMNS_PER_SBOX_AES][HEX_STRING_SIZE] = {
	{ "63", "7c", "77", "7b", "f2", "6b", "6f", "c5", "30", "01", "67", "2b", "fe", "d7", "ab", "76" },
	{ "ca", "82", "c9", "7d", "fa", "59", "47", "f0", "ad", "d4", "a2", "af", "9c", "a4", "72", "c0" },
	{ "b7", "fd", "93", "26", "36", "3f", "f7", "cc", "34", "a5", "e5", "f1", "71", "d8", "31", "15" },
	{ "04", "c7", "23", "c3", "18", "96", "05", "9a", "07", "12", "80", "e2", "eb", "27", "b2", "75" },
	{ "09", "83", "2c", "1a", "1b", "6e", "5a", "a0", "52", "3b", "d6", "b3", "29", "e3", "2f", "84" },
	{ "53", "d1", "00", "ed", "20", "fc", "b1", "5b", "6a", "cb", "be", "39", "4a", "4c", "58", "cf" },
	{ "d0", "ef", "aa", "fb", "43", "4d", "33", "85", "45", "f9", "02", "7f", "50", "3c", "9f", "a8" },
	{ "51", "a3", "40", "8f", "92", "9d", "38", "f5", "bc", "b6", "da", "21", "10", "ff", "f3", "d2" },
	{ "cd", "0c", "13", "ec", "5f", "97", "44", "17", "c4", "a7", "7e", "3d", "64", "5d", "19", "73" },
	{ "60", "81", "4f", "dc", "22", "2a", "90", "88", "46", "ee", "b8", "14", "de", "5e", "0b", "db" },
	{ "e0", "32", "3a", "0a", "49", "06", "24", "5c", "c2", "d3", "ac", "62", "91", "95", "e4", "79" },
	{ "e7", "c8", "37", "6d", "8d", "d5", "4e", "a9", "6c", "56", "f4", "ea", "65", "7a", "ae", "08" },
	{ "ba", "78", "25", "2e", "1c", "a6", "b4", "c6", "e8", "dd", "74", "1f", "4b", "bd", "8b", "8a" },
	{ "70", "3e", "b5", "66", "48", "03", "f6", "0e", "61", "35", "57", "b9", "86", "c1", "1d", "9e" },
	{ "e1", "f8", "98", "11", "69", "d9", "8e", "94", "9b", "1e", "87", "e9", "ce", "55", "28", "df" },
	{ "8c", "a1", "89", "0d", "bf", "e6", "42", "68", "41", "99", "2d", "0f", "b0", "54", "bb", "16" }
};

static const char INVERSE_SBOX[ROWS_PER_SBOX_AES][COLUMNS_PER_SBOX_AES][HEX_STRING_SIZE] = {
	{ "52", "09", "6a", "d5", "30", "36", "a5", "38", "bf", "40", "a3", "9e", "81", "f3", "d7", "fb" },
	{ "7c", "e3", "39", "82", "9b", "2f", "ff", "87", "34", "8e", "43", "44", "c4", "de", "e9", "cb" },
	{ "54", "7b", "94", "32", "a6", "c2", "23", "3d", "ee", "4c", "95", "0b", "42", "fa", "c3", "4e" },
	{ "08", "2e", "a1", "66", "28", "d9", "24", "b2", "76", "5b", "a2", "49", "6d", "8b", "d1", "25" },
	{ "72", "f8", "f6", "64", "86", "68", "98", "16", "d4", "a4", "5c", "cc", "5d", "65", "b6", "92" },
	{ "6c", "70", "48", "50", "fd", "ed", "b9", "da", "5e", "15", "46", "57", "a7", "8d", "9d", "84" },
	{ "90", "d8", "ab", "00", "8c", "bc", "d3", "0a", "f7", "e4", "58", "05", "b8", "b3", "45", "06" },
	{ "d0", "2c", "1e", "8f", "ca", "3f", "0f", "02", "c1", "af", "bd", "03", "01", "13", "8a", "6b" },
	{ "3a", "91", "11", "41", "4f", "67", "dc", "ea", "97", "f2", "cf", "ce", "f0", "b4", "e6", "73" },
	{ "96", "ac", "74", "22", "e7", "ad", "35", "85", "e2", "f9", "37", "e8", "1c", "75", "df", "6e" },
	{ "47", "f1", "1a", "71", "1d", "29", "c5", "89", "6f", "b7", "62", "0e", "aa", "18", "be", "1b" },
	{ "fc", "56", "3e", "4b", "c6", "d2", "79", "20", "9a", "db", "c0", "fe", "78", "cd", "5a", "f4" },
	{ "1f", "dd", "a8", "33", "88", "07", "c7", "31", "b1", "12", "10", "59", "27", "80", "ec", "5f" },
	{ "60", "51", "7f", "a9", "19", "b5", "4a", "0d", "2d", "e5", "7a", "9f", "93", "c9", "9c", "ef" },
	{ "a0", "e0", "3b", "4d", "ae", "2a", "f5", "b0", "c8", "eb", "bb", "3c", "83", "53", "99", "61" },
	{ "17", "2b", "04", "7e", "ba", "77", "d6", "26", "e1", "69", "14", "63", "55", "21", "0c", "7d" }
};

static const char MIX_COLUMN_MATRIX[BYTES_PER_WORD][BYTES_PER_WORD][HEX_STRING_SIZE] = {
	{ "02", "03", "01", "01" },
	{ "01", "02", "03", "01" },
	{ "01", "01", "02", "03" },
	{ "03", "01", "01", "02" }
};

static const char INV_MIX_COLUMN_MATRIX[BYTES_PER_WORD][BYTES_PER_WORD][HEX_STRING_SIZE] = {
	{ "0E", "0B", "0D", "09" },
	{ "09", "0E", "0B", "0D" },
	{ "0D", "09", "0E", "0B" },
	{ "0B", "0D", "09", "0E" }
};


#endif