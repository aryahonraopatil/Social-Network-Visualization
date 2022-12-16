#Author: Salem Soin-Voshell
#File: networkgen.R
#Description: Used to generate social networks that are tied to geographical points, using a csv of cities
#around the world.

#Inputs
num_nodes = 100
edges_min = 5 #AVG
edges_max = 15

cities <- read.csv("../../datasets/worldcities.csv")


#Attribute List
#Following
#Location
#Followers
#city name
#long
#lat
#Post Count #1-100, weighted lower

df <- data.frame (index  = c(0),
                  location = c("Abu Dhabi"),
                  follower_count = c(34),
                  following_count = c(100),
                  long = c(0),
                  lat = c(0),
                  post_count = c(1))

for(i in 1:num_nodes){
  #following_list = sample(1:num_nodes, sample(edges_min:edges_max, 1 , replace = FALSE), replace = FALSE)
  #Check that self is not in following list
  rand_city = cities[sample(1:nrow(cities), 1),]
  df = rbind(df, data.frame (index  = c(i),
                             location = c(rand_city$city_ascii),
                             follower_count = c(sample(1:1000, 1)[1]),
                             following_count = c(sample(edges_min:edges_max, 1)[1]),
                             long = c(rand_city$lng),
                             lat = c(rand_city$lat),
                             post_count = c(sample(1:100, 1)[1])))
}

df = df[-1,]


df2 <- data.frame(account = c(0),
                  following = c(1))

for(i in 1:num_nodes){
  following_list = sample(1:num_nodes, df[i, ]$following_count, replace = FALSE)
  while(i %in% following_list){
    following_list = sample(1:num_nodes, df[i, ]$following_count, replace = FALSE)
  }
  df2 = rbind(df2, data.frame(account = c(i),
                              following = c(following_list)))
}

df2 = df2[-1,]

write.csv(df2, "edges.csv", row.names = FALSE)

df$DFC <- -1
df$DFC[1] <- 0



for(l in 1:nrow(df2)){
  if(df[(df2[l,]$account),]$DFC != -1){
    if(df[(df2[l,]$following),]$DFC == -1){
      df[df2[l,]$following,]$DFC <- df[df2[l,]$account,]$DFC + 1
    }
    else if(df[df2[l,]$following,]$DFC > df[df2[l,]$account,]$DFC + 1){
      df[df2[l,]$following,]$DFC <- df[df2[l,]$account,]$DFC + 1
    }
  }
}

write.csv(df, "accounts.csv", row.names = FALSE)
