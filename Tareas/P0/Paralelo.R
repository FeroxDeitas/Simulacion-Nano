library(parallel)

cluster = makeCluster(detectCores(logical=FALSE) - 1)
desde = 3
hasta = 69
base = 6

clusterExport(cluster, "base")

parSapply(cluster, desde:hasta, function(x) base^x)
parSapply(cluster, desde:hasta, function(x) 2^x)

stopCluster(cluster)
