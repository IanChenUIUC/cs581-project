#!/usr/bin/env bash

### Create ~300 jobs to run all methods on all datasets in parallel
### Sets three "model" and "replicate" variables for the sbatch file

# ==============================================================================
# MAGUS (default)
# ==============================================================================

# All ROSE conditions and replicates
for r in {0..9}
do
	_rose_models=( "1000M2" "1000M3" "1000L1" "1000L2" "1000L3" )
	for rose in ${_rose_models[@]}
	do
		rose_models=( $rose )
		rose_replis=($(seq $r 1 $r))
		ROSE_MODELS=$(IFS=,; echo "${rose_models[@]}") ROSE_REPLIS=$(IFS=,; echo "${rose_replis[@]}") method="magus_default" sbatch method_secondary.sbatch
	done
done

# All RNASim 1000 replicates
for r in {0..9}
do
	rnasim_models=( "1000" )
	rnasim_replis=($(seq $r 1 $r))
	RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="magus_default" sbatch method_secondary.sbatch
done

# All RNASim 1000 replicates
for r in {0..9}
do
	rnasim_models=( "10000" )
	rnasim_replis=($(seq $r 1 $r))
	RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="magus_default" sbatch method.sbatch
done

# All 16S conditions
s_models=( "16S.3" "16S.T" "16S.M" "16S.B.ALL" )
S_MODELS=$(IFS=,; echo "${s_models[@]}") method="magus_default" sbatch method.sbatch

# ==============================================================================
# MAGUS (magus initial, with 4 iterations)
# ==============================================================================

# All ROSE conditions and replicates
for r in {0..9}
do
	_rose_models=( "1000M2" "1000M3" "1000L1" "1000L2" "1000L3" )
	for rose in ${_rose_models[@]}
	do
		rose_models=( $rose )
		rose_replis=($(seq $r 1 $r))
		ROSE_MODELS=$(IFS=,; echo "${rose_models[@]}") ROSE_REPLIS=$(IFS=,; echo "${rose_replis[@]}") method="magus_magus" sbatch method_secondary.sbatch
	done
done

# All RNASim 1000 replicates
for r in {0..9}
do
	rnasim_models=( "1000" )
	rnasim_replis=($(seq $r 1 $r))
	RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="magus_magus" sbatch method_secondary.sbatch
done

# All RNASim 10000 replicates
for r in {0..9}
do
	rnasim_models=( "10000" )
	rnasim_replis=($(seq $r 1 $r))
	RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="magus_magus" sbatch method.sbatch
done

# 16S besides B.ALL
s_models=( "16S.3" "16S.T" "16S.M" )
S_MODELS=$(IFS=,; echo "${s_models[@]}") method="magus_magus" sbatch method.sbatch

# 16S B.ALL
s_models=( "16S.B.ALL" )
S_MODELS=$(IFS=,; echo "${s_models[@]}") method="magus_magus" sbatch method.sbatch

# ==============================================================================
# MAGUS (clustalo initial, with 4 iterations)
# ==============================================================================

# All ROSE conditions and replicates
for r in {0..9}
do
	_rose_models=( "1000M2" "1000M3" "1000L1" "1000L2" "1000L3" )
	for rose in ${_rose_models[@]}
	do
		rose_models=( $rose )
		rose_replis=($(seq $r 1 $r))
		ROSE_MODELS=$(IFS=,; echo "${rose_models[@]}") ROSE_REPLIS=$(IFS=,; echo "${rose_replis[@]}") method="magus_clustalo" sbatch method_secondary.sbatch
	done
done

# All RNASim 1000 replicates
for r in {0..9}
do
	rnasim_models=( "1000" )
	rnasim_replis=($(seq $r 1 $r))
	RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="magus_clustalo" sbatch method_secondary.sbatch
done

# All RNASim 10000 replicates
for r in {0..9}
do
	rnasim_models=( "10000" )
	rnasim_replis=($(seq $r 1 $r))
	RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="magus_clustalo" sbatch method.sbatch
done

# 16S besides B.ALL
s_models=( "16S.3" "16S.T" "16S.M" )
S_MODELS=$(IFS=,; echo "${s_models[@]}") method="magus_clustalo" sbatch method.sbatch

# 16S B.ALL
s_models=( "16S.B.ALL" )
S_MODELS=$(IFS=,; echo "${s_models[@]}") method="magus_clustalo" sbatch method.sbatch

# ==============================================================================
# PASTA (default, with 1-3 iterations)
# ==============================================================================

# All ROSE conditions and replicates
for r in {0..9}
do
	_rose_models=( "1000M2" "1000M3" "1000L1" "1000L2" "1000L3" )
	for rose in ${_rose_models[@]}
	do
		rose_models=( $rose )
		rose_replis=($(seq $r 1 $r))
		ROSE_MODELS=$(IFS=,; echo "${rose_models[@]}") ROSE_REPLIS=$(IFS=,; echo "${rose_replis[@]}") method="pasta" sbatch method_secondary.sbatch
	done
done

# All RNASim 1000 replicates
rnasim_models=( "1000" )
rnasim_replis=($(seq 0 1 4))
RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="pasta" sbatch method.sbatch

rnasim_models=( "1000" )
rnasim_replis=($(seq 5 1 9))
RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="pasta" sbatch method.sbatch

# All RNASim 10000 replicates
for r in {0..9}
do
	rnasim_models=( "10000" )
	rnasim_replis=($(seq $r 1 $r))
	RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="pasta" sbatch method.sbatch
done

# 16S besides B.ALL
s_models=( "16S.3" "16S.T" "16S.M" )
S_MODELS=$(IFS=,; echo "${s_models[@]}") method="pasta" sbatch method.sbatch

# 16S B.ALL
s_models=( "16S.B.ALL" )
S_MODELS=$(IFS=,; echo "${s_models[@]}") method="pasta" sbatch method.sbatch

# ==============================================================================
# MUSCLE
# ==============================================================================

# All ROSE conditions and replicates
for r in {0..9}
do
	rose_models=( "1000M2" "1000M3" )
	rose_replis=($(seq $r 1 $r))
	ROSE_MODELS=$(IFS=,; echo "${rose_models[@]}") ROSE_REPLIS=$(IFS=,; echo "${rose_replis[@]}") method="muscle" sbatch method_secondary.sbatch

	rose_models=( "1000L1" "1000L2" )
	rose_replis=($(seq $r 1 $r))
	ROSE_MODELS=$(IFS=,; echo "${rose_models[@]}") ROSE_REPLIS=$(IFS=,; echo "${rose_replis[@]}") method="muscle" sbatch method_secondary.sbatch

	rose_models=( "1000L3" )
	rose_replis=($(seq $r 1 $r))
	ROSE_MODELS=$(IFS=,; echo "${rose_models[@]}") ROSE_REPLIS=$(IFS=,; echo "${rose_replis[@]}") method="muscle" sbatch method_secondary.sbatch
done

# All RNASim 1000 replicates
for r in {0..9}
do
	rnasim_models=( "1000" )
	rnasim_replis=($(seq $r 1 $r))
	RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="muscle" sbatch method_secondary.sbatch
done

# All RNASim 10000 replicates
for r in {0..9}
do
	rnasim_models=( "10000" )
	rnasim_replis=($(seq $r 1 $r))
	RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="muscle" sbatch method.sbatch
done

# 16S besides B.ALL
s_models=( "16S.3" "16S.T" "16S.M" )
S_MODELS=$(IFS=,; echo "${s_models[@]}") method="muscle" sbatch method.sbatch

# 16S B.ALL
s_models=( "16S.B.ALL" )
S_MODELS=$(IFS=,; echo "${s_models[@]}") method="muscle" sbatch method.sbatch

# ==============================================================================
# MAFFT (-auto)
# ==============================================================================

# All ROSE conditions and replicates
rose_models=( "1000M2" "1000M3" "1000L1" "1000L2" "1000L3" )
rose_replis=($(seq 0 1 9))
rnasim_models=( "1000" "10000" )
rnasim_replis=($(seq 0 1 9))
s_models=( "16S.3" "16S.T" "16S.M" "16S.B.ALL" )
ROSE_MODELS=$(IFS=,; echo "${rose_models[@]}") ROSE_REPLIS=$(IFS=,; echo "${rose_replis[@]}") RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") S_MODELS=$(IFS=,; echo "${s_models[@]}") method="mafft" sbatch method.sbatch

# ==============================================================================
# ClustalOmega (-auto)
# ==============================================================================

# All ROSE conditions and replicates
for r in {0..9}
do
	rose_models=( "1000M2" "1000M3" "1000L1" "1000L2" "1000L3" )
	rose_replis=($(seq $r 1 $r))
	ROSE_MODELS=$(IFS=,; echo "${rose_models[@]}") ROSE_REPLIS=$(IFS=,; echo "${rose_replis[@]}") method="clustalo" sbatch method_secondary.sbatch
done

# All RNASim 1000 replicates
for r in {0..9}
do
	rnasim_models=( "1000" )
	rnasim_replis=($(seq $r 1 $r))
	RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="clustalo" sbatch method_secondary.sbatch
done

# All RNASim 10K replicates
for r in {0..9}
do
	rnasim_models=( "10000" )
	rnasim_replis=($(seq $r 1 $r))
	RNASim_MODELS=$(IFS=,; echo "${rnasim_models[@]}") RNASim_REPLIS=$(IFS=,; echo "${rnasim_replis[@]}") method="clustalo" sbatch method.sbatch
done

# All 16S conditions
s_models=( "16S.3" "16S.T" "16S.M" "16S.B.ALL" )
S_MODELS=$(IFS=,; echo "${s_models[@]}") method="clustalo" sbatch method.sbatch
