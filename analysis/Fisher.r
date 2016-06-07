data <- matrix(c(9,17,20,8,12,27), ncol=3, byrow=T) 
# Contingency Table 
fisher.test(data) 
library(vcd) 
assocstats(data) 
