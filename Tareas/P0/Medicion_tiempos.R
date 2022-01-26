for (n in 8:13) {
k=2^n; cat(n, k, system.time(matrix(runif(k*k),ncol=k))[3], '\n')
}