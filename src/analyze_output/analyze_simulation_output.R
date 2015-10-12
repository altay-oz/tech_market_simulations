### this file analyzes the output of simulations carried out under
### different alpha and beta values
### http://igraph.org/c/doc/igraph-Structural.html
library(igraph)
library(ggplot2)

setwd("../../../")

output.directories <- dir(pattern = "^output_")

## create an empty data frame for learning, cumulative knowledge etc.
agent.cycle <- data.frame()
agent <- data.frame()
agent.alliance <- data.frame()
network.data <- data.frame()

################################################
## load all data files and create data frames
for (output.dir in output.directories) {
    setwd(output.dir)

    ####################    
    ## get the alpha and beta values
    alpha.beta <- read.csv(file="alpha_beta_file.txt", head=FALSE, sep=",")
    alpha <- alpha.beta[,1]
    beta <- alpha.beta[,2]
    
    ## load all data in the directory

    ####################    
    ## run, cycle, agent_id, market_location, tech_location, cum_knowledge, cycle_realized_learning
    agent.cycle.tmp <- read.csv(file="data_agent_cycle.txt", head=TRUE, sep=",")

    ## adding alpha and beta values
    agent.cycle.tmp$alpha <- alpha
    agent.cycle.tmp$beta <- beta

    ## remove the columns related to agents' places on the map
    agent.cycle.tmp$map_market <- NULL
    agent.cycle.tmp$map_knowledge <- NULL

    ####################    
    ## run, cycle, agent_id, entry_cycle, sigma_m, sigma_k
    agent.tmp <- read.csv(file="data_agent.txt", head=TRUE, sep=",")

    ## adding alpha and beta values
    agent.tmp$alpha <- alpha
    agent.tmp$beta <- beta

    ## add firm_type. This depends on sigma_m and sigma_t. There are 4 types of firms.
    ## max(sigma_m/k) = 3.
    ## sigma_k is in fact sigma_technology. 
    agent.tmp$type[ agent.tmp$sigma_m < 1.5 & agent.tmp$sigma_k < 1.5 ]   <- 'I' 
    agent.tmp$type[ agent.tmp$sigma_m < 1.5 & agent.tmp$sigma_k >= 1.5 ]  <- 'II'
    agent.tmp$type[ agent.tmp$sigma_m >= 1.5 & agent.tmp$sigma_k >= 1.5 ] <- 'III'
    agent.tmp$type[ agent.tmp$sigma_m >= 1.5 & agent.tmp$sigma_k < 1.5 ]  <- 'IV'
    
    ## removing four columns, they are not needed anymore.
    agent.tmp$cycle <- NULL
    agent.tmp$entry_cycle <- NULL ## there is no entry during the simulations all = 0.

    ####################    
    ## run, cycle, agent_id1, agent_id2
    agent.alliance.tmp <- read.csv(file="data_alliance.txt", head=TRUE, sep=",")

    ## adding alpha and beta values
    agent.alliance.tmp$alpha <- alpha
    agent.alliance.tmp$beta <- beta

    ####################
    ## run, cycle, number_of_agents, network_total_cum_knowledge, network_total_realized_learning,
    ## average_agent_cum_knowledge, average_agent_realized_learning,
    ## min_agent_cum_knowledge, max_agent_cum_knowledge
    network.data.tmp <- read.csv(file="data_network.txt", head=TRUE, sep=",")

    ## adding alpha and beta values
    network.data.tmp$alpha <- alpha
    network.data.tmp$beta <- beta

    ## rbind all 4 data sets with alpha and beta and some removed columns
    ## these four data frames will be used in further analysis
    agent.cycle <- rbind(agent.cycle, agent.cycle.tmp)
    agent <- rbind(agent, agent.tmp)
    agent.alliance <- rbind(agent.alliance, agent.alliance.tmp)
    network.data <- rbind(network.data, network.data.tmp)

    setwd("../")
} # directories end of the loop

## remove objects for memory
rm(list=c("agent.alliance.tmp", "agent.cycle.tmp", "agent.tmp", "network.data.tmp", "alpha", "beta", "alpha.beta", "output.dir", "output.directories"))

## check column names
names(agent)
names(agent.alliance)
names(agent.cycle)
names(network.data)

## change column names to std R code.
colnames(agent) <- c("run", "agent.id", "sigma.m", "sigma.k", "alpha", "beta", "type")
colnames(agent.alliance) <- c("run", "cycle", "agent.id.1", "agent.id.2", "alpha", "beta")
colnames(agent.cycle) <- c("run", "cycle", "agent.id", "cum.knowledge",
                           "cycle.realized.learning", "alpha", "beta")
colnames(network.data) <- c("run", "cycle", "number.of.agents", "network.total.cum.knowledge",
                            "network.total.realized.learning", "average.agent.cum.knowledge",
                            "average.agent.realized.learning", "min.agent.cum.knowledge",
                            "max.agent.cum.knowledge", "alpha", "beta")
 
## used in the loops
alpha.df <- unique(agent$alpha)
beta.df <- unique(agent$beta)
run.df <- unique(agent$run)
max.run <- max(agent$run)
cycle.seq.10 <- seq(0, 500, by = 10)
cycle.seq <- seq(1, 500)
firm.type.list <- c("I","II","III","IV")

######################################################################
##################      knowledge part    ############################
######################################################################

## with this we are adding the firm type for each agent in agent.cycle dataframe under agent_cycle_type df.

if (file.exists('./agent_cycle_type.txt')) {
    agent.cycle.type <- dget('./agent_cycle_type.txt')
} else {
    agent.cycle.type <- merge(agent.cycle, agent, by = c("run", "agent.id", "alpha", "beta"))
    dput(agent.cycle.type, file='./agent_cycle_type.txt')
}

learning.knowledge.data <- data.frame()

if (file.exists('./learn_know_data.txt')) {
    learning.knowledge.data <- dget('./learn_know_data.txt')
} else {
      for (a in alpha.df) {
          for (b in beta.df) {
              for (cycle.no in cycle.seq.10) {
                  control <- c(a, b, cycle.no)
                  print(control)
                  for (firm.type in firm.type.list) {
                      ## obtain the subset for a definite cycle and firm.type
                      analyzed.subset <- subset(agent.cycle.type, cycle==cycle.no &
                                                                  type==firm.type & alpha==a & beta==b)
                      ## calculate the average of cumulated knowledge and cyclic learning
                      avg.knowledge <- mean(analyzed.subset$cum.knowledge)
                      avg.cyclic.learning <- mean(analyzed.subset$cycle.realized.learning)
                      ## create the data frame
                      cycle.data <- data.frame(cycle.no, a, b, firm.type, avg.knowledge, avg.cyclic.learning)
                      ## insert the data vector to use in graphics
                      learning.knowledge.data <- rbind(learning.knowledge.data, cycle.data)
                  }
              }
          }
      }
      dput(learning.knowledge.data, file='./learn_know_data.txt')
}


############################################################
# --------------- CREATE GRAPHICS --------------------------
##################   knowledge   ###########################
############################################################

## obtain the last (max, cycle.no==500) knowledge values for each firm types,
## remove the col avg_cyclic_learning
learning.know.subset <- subset(learning.knowledge.data, cycle.no==500, select=-c(avg.cyclic.learning))
## remove the rownames
rownames(learning.know.subset) <- NULL

## remove the cycle.no column
## learning.know.subset$cycle.no <- NULL
learning.know.subset <- subset(learning.know.subset, select=-c(cycle.no))

## create an empty data frame for all alpha, beta and avg_know values to create a tile figure.
ab.know.data <- data.frame(a = double(), b = double(), avg.know = double())

for (alpha in alpha.df) {
    for (beta in beta.df) {
        avg.know.list <- learning.know.subset$avg.knowledge[learning.know.subset$a==alpha &
                                                            learning.know.subset$b==beta]
        avg.know <- mean(avg.know.list)
        ab.know.data <- rbind(ab.know.data, c(alpha, beta, avg.know))
    }
}

colnames(ab.know.data) <- c("alpha", "beta", "avg.know")

learning.total <- ggplot(ab.know.data, aes(x=beta, y=alpha)) +
                         geom_tile(aes(fill=avg.know)) +
                        theme(legend.title=element_blank()) +
                        ggtitle("Avg. accumulated knowledge") +
                        xlab(expression(beta)) +
                        ylab(expression(alpha))
learning.total

ggsave(filename="tile_learning_total.pdf")

##############################################
### line graph learning v. cycle, figure 2
### x -> cycle num [0,500], y -> avg.learning

### loop on distinct alpha and beta and construct line graph on knowldege v. cycle
for (a in alpha.df) {
    for (b in beta.df) {
        # create a subset of data to plot
        learn.know.a.b <- subset(learning.knowledge.data, alpha==a & beta==b)

        title <- paste("Accumulated knowledge / agent  (alpha = ", a, " beta = ", b,")")
    
        cyclic.know <- ggplot(learn.know.a.b,
                                  aes(x=cycle.no, y=avg.knowledge, group=firm.type, colour=factor(firm.type))) +
                                    geom_line() +
                                    ylab("acc. knowledge / agent") +
                                    xlab("cycle") +
                                    expand_limits(y=c(0, 1400)) +
                                    scale_y_continuous(breaks=seq(0, 1400, 200)) +
                                    theme(legend.title=element_blank()) +                    
                                    ggtitle(title)
        cyclic.know
         
        fname <- paste("learning_in_cycle_alpha_", alpha, "_beta_", beta, ".pdf", sep="")
        ggsave(filename=fname)
    }
}


##############################################
### distribution of accumulated knowledge of firms wrt. sigma t and m. at the last cycle

names(agent)
names(agent.cycle)

## needed; at cycle 500; alpha, beta, avg(cum.knowledge)
agent.cycle500 <- subset(agent.cycle, cycle==500)

## merge agent and agent.cycle
agent.cycle500.sigmas <- merge(agent.cycle500, agent, all=TRUE)

names(agent.cycle500.sigmas)
      
for (a in alpha.df) {
    for (b in beta.df) {
        analyzed.subset <- subset(agent.cycle500.sigmas, alpha==a & beta==b)

        title <- paste("Accumulated knowledge (alpha = ", a, " beta = ", b,")")

        a.b.cum.know.500 <- ggplot(analyzed.subset, aes(sigma.m, sigma.k)) +
                              geom_point(aes(size=cum.knowledge, colour="#999999")) +
                              ggtitle(title) +
                              ylab("sigma tech.") +
                              xlab("sigma market") +
                              theme(legend.position="none") 
        a.b.cum.know.500

        fname <- paste("acc_knowledge_", alpha, "_beta_", beta, ".pdf", sep="")
        ggsave(filename=fname)
    }
}

names(agent.cycle500)

## trellis for acc.knowledge at the end of sim.
a.b.cum.know.500.trellis <- ggplot(agent.cycle500.sigmas, aes(sigma.m, sigma.k)) +
                              geom_point(aes(size=cum.knowledge), colour="grey60") +
                              facet_grid(alpha ~ beta, as.table=FALSE) +
                              ylab("sigma tech.") +
                              xlab("sigma market") +
                              theme(legend.position="none") 
a.b.cum.know.500.trellis

ggsave('./cum_knowledge_at500_trellis.pdf')


## loop on distinct alpha and beta and construct line graph on knowldege v. cycle
for (a in alpha.df) {
    for (b in beta.df) {
        # create a subset of data to plot
        learn.know.a.b <- subset(learning.knowledge.data, alpha==a & beta==b)

        title <- paste("Accumulated knowledge / agent  (alpha = ", a, " beta = ", b,")")
    
        cyclic.know <- ggplot(learn.know.a.b,
                                  aes(x=cycle.no, y=avg.knowledge, group=firm.type, colour=factor(firm.type))) +
                                    geom_line() +
                                    ylab("acc. knowledge / agent") +
                                    xlab("cycle") +
                                    expand_limits(y=c(0, 1400)) +
                                    scale_y_continuous(breaks=seq(0, 1400, 200)) +
                                    theme(legend.title=element_blank()) +                    
                                    ggtitle(title)
        cyclic.know
         
        fname <- paste("learning_in_cycle_alpha_", alpha, "_beta_", beta, ".pdf", sep="")
        ggsave(filename=fname)
    }
}



#######################################
### trellis graph for knowledge and cycle

## TODO mention alpha and beta on sub x and y. ; check the directlabel package
cyclic.know.trellis <- ggplot(learning.knowledge.data,
                              aes(x=cycle.no, y=avg.knowledge, group=firm.type, colour=factor(firm.type))) +
                              geom_line() +
                              facet_grid(a ~ b, , as.table = FALSE) +
                              expand_limits(y=c(0,1500)) +
                              scale_y_continuous("average cummulated knowledge / agent",
                                                 breaks=seq(0,1500,300)) +
                              scale_x_continuous("cycle") +
                              theme(legend.title=element_blank())
cyclic.know.trellis
        
ggsave('./cum_knowledge_trellis.pdf')

###############################################
### trellis graph acc. learning v. cycle

### TODO  mention alpha and beta on sub x and y.
cyclic.learn.trellis <- ggplot(learning.knowledge.data, 
                               aes(x=cycle.no, y=avg.cyclic.learning,
                                   group=firm.type, colour=factor(firm.type))) +
                              geom_line() +
                              facet_grid(a ~ b, as.table = FALSE) +
                              expand_limits(y=c(0,15)) +
                              scale_y_continuous("average learning / agent", breaks=seq(0,15,5)) +
                              scale_x_continuous("cycle") +
                              theme(legend.title=element_blank())
cyclic.learn.trellis
        
ggsave('./learning_in_cycle_trellis.pdf')

##########################################################################
##########################################################################
#-------------------   NETWORK PART  -------------------------------------
##########################################################################
##########################################################################

if (file.exists('./agent_alliance_data.txt')) {
    agent.alliance.data <- dget('./agent_alliance_data.txt')
} else {
    ### adding the firm type column for the two columns(dyadic network)
    agent.all.temp1 <- merge(agent.alliance, agent, by.x = c("run", "alpha", "beta", "agent.id.1"),
                             by.y = c("run", "alpha", "beta", "agent.id"))
    colnames(agent.all.temp1)[7] <- c("type.1")
    agent.alliance.data <- merge(agent.all.temp1, agent, by.x = c("run", "alpha", "beta", "agent.id.2"),
                                 by.y = c("run", "alpha", "beta", "agent.id"))
    colnames(agent.alliance.data)[8] <- c("type.2")

    dput(agent.alliance.data, file='./agent_alliance_data.txt')
}

##########################################
### counting inter firm-type links
##########################################

## count total ties later on by adding up all data calculated for each cycle
## compare it wrt to the next for-loop, or other images obtained before.

num.ties.data.a.b <- data.frame()
num.ties.data.g4 <- matrix(ncol=5)
num.ties.data.inter.firm <- matrix(ncol=5)

if (file.exists('./num_ties_data_g4.txt') & file.exists('./num_ties_data_inter_firm.txt')) {
    num.ties.data.g4 <- dget('./num_ties_data_g4.txt')
    num.ties.data.inter.firm <- dget('./num_ties_data_inter_firm.txt')
} else {
    for (c in cycle.seq) {
        for (a in alpha.df) {
            for (b in beta.df) {
                ## obtain the subset for a definite cycle, firm.type
                agent.alliance.subset <- subset(agent.alliance.data, alpha == a & beta == b & cycle == c)
                control <- c(a, b, c)
                print(control)
                
                ## the file contain both a-b and b-a ties thus counting only a single column is OK.
                ## valid only for 4g comparisons, counting the ties that are made by I, II, III, IV type firms.
                count.firm.types <- table(agent.alliance.subset$type.1)

                ## for bar charts, data.frame(a, b, firm.type, link_count)
                for (firm.type in firm.type.list) {
                    ## counting link numbers for each firm types.
                    link.count <- count.firm.types[names(count.firm.types)==firm.type] / max.run
                    num.ties.g4 <- c(a, b, c, firm.type, link.count)
                    print(num.ties.g4)
                    num.ties.data.g4 <- rbind(num.ties.data.g4, num.ties.g4)
                }

                ## ---- number of ties between groups.--------------------------------------
                inter.firm.ties.table <- table(agent.alliance.subset$type.1, agent.alliance.subset$type.2)
                inter.firm.ties.df <- data.frame(inter.firm.ties.table)

                count.1.1 <- subset(inter.firm.ties.df, Var1=="I" & Var2 == "I")$Freq / max.run
                num.ties.data.inter.firm <- rbind(num.ties.data.inter.firm, c(a, b, c, "I-I", count.1.1))
                
                count.2.2 <- subset(inter.firm.ties.df, Var1=="II" & Var2 == "II")$Freq / max.run
                num.ties.data.inter.firm <- rbind(num.ties.data.inter.firm, c(a, b, c, "II-II", count.2.2))
                
                count.3.3 <- subset(inter.firm.ties.df, Var1=="III" & Var2 == "III")$Freq / max.run
                num.ties.data.inter.firm <- rbind(num.ties.data.inter.firm, c(a, b, c, "III-III", count.3.3))
                
                count.4.4 <- subset(inter.firm.ties.df, Var1=="IV" & Var2 == "IV")$Freq / max.run
                num.ties.data.inter.firm <- rbind(num.ties.data.inter.firm, c(a, b, c, "IV-IV", count.4.4))
                
                count.1.2 <- subset(inter.firm.ties.df, Var1=="I" & Var2 == "II")$Freq / max.run
                num.ties.data.inter.firm <- rbind(num.ties.data.inter.firm, c(a, b, c, "I-II", count.1.2))
                
                count.1.3 <- subset(inter.firm.ties.df, Var1=="I" & Var2 == "III")$Freq / max.run
                num.ties.data.inter.firm <- rbind(num.ties.data.inter.firm, c(a, b, c, "I-III", count.1.3))

                count.1.4 <- subset(inter.firm.ties.df, Var1=="I" & Var2 == "IV")$Freq / max.run
                num.ties.data.inter.firm <- rbind(num.ties.data.inter.firm, c(a, b, c, "I-IV", count.1.4))
                
                count.2.3 <- subset(inter.firm.ties.df, Var1=="II" & Var2 == "III")$Freq / max.run
                num.ties.data.inter.firm <- rbind(num.ties.data.inter.firm, c(a, b, c, "II-III", count.2.3))

                count.2.4 <- subset(inter.firm.ties.df, Var1=="II" & Var2 == "IV")$Freq / max.run
                num.ties.data.inter.firm <- rbind(num.ties.data.inter.firm, c(a, b, c, "II-IV", count.2.4))
                
                count.3.4 <- subset(inter.firm.ties.df, Var1=="III" & Var2 == "IV")$Freq / max.run
                num.ties.data.inter.firm <- rbind(num.ties.data.inter.firm, c(a, b, c, "III-IV", count.3.4))
            } # alpha
        } # beta
    } # cycle
    dput(num.ties.data.g4, file='./num_ties_data_g4.txt')
    dput(num.ties.data.inter.firm, file='./num_ties_data_inter_firm.txt')
} # file.exists

head(num.ties.data.g4)
nrow(num.ties.data.g4)

num.ties.data.g4 <- num.ties.data.g4[-1,]
num.ties.data.g4 <- as.data.frame(num.ties.data.g4)
rownames(num.ties.data.g4) <- NULL
colnames(num.ties.data.g4) <- c("alpha", "beta", "cycle", "firm.type", "link.count")

num.ties.data.g4$alpha <- as.numeric(levels(num.ties.data.g4$alpha))[num.ties.data.g4$alpha]
num.ties.data.g4$beta <- as.numeric(levels(num.ties.data.g4$beta))[num.ties.data.g4$beta]
num.ties.data.g4$cycle <- as.numeric(levels(num.ties.data.g4$cycle))[num.ties.data.g4$cycle]
num.ties.data.g4$link.count <- as.numeric(levels(num.ties.data.g4$link.count))[num.ties.data.g4$link.count]


head(num.ties.data.inter.firm)
nrow(num.ties.data.inter.firm)

num.ties.data.inter.firm <- num.ties.data.inter.firm[-1,]
num.ties.data.inter.firm <- as.data.frame(num.ties.data.inter.firm)
rownames(num.ties.data.inter.firm) <- NULL
colnames(num.ties.data.inter.firm) <- c("alpha", "beta", "cycle", "interfirm.tie.type", "tie.count")

num.ties.data.inter.firm$alpha <- as.numeric(levels(num.ties.data.inter.firm$alpha))[num.ties.data.inter.firm$alpha]
num.ties.data.inter.firm$beta <- as.numeric(levels(num.ties.data.inter.firm$beta)) [num.ties.data.inter.firm$beta]
num.ties.data.inter.firm$cycle <- as.numeric(levels(num.ties.data.inter.firm$cycle))[num.ties.data.inter.firm$cycle]
num.ties.data.inter.firm$tie.count <- as.numeric(levels(num.ties.data.inter.firm$tie.count))[num.ties.data.inter.firm$tie.count]



######################################################################################
##########################################
### GRAPH for link numbers
##########################################

#######################################
### trellis graph for 4 groups link number
num.ties.g4.total <- data.frame()

for (a in alpha.df) {
    for (b in beta.df) {
        subset.num.ties.g4 <- subset(num.ties.data.g4, alpha == a & beta == b)
        total.tie <- sum(subset.num.ties.g4$link.count)
        num.tie.total <- data.frame(a, b, total.tie)
        num.ties.g4.total <- rbind(num.ties.g4.total, num.tie.total)
    }
}

## beware of division by 100
links.ties <- ggplot(num.ties.g4.total, aes(x=b, y=a)) +
                       geom_tile(aes(fill=total.tie/100)) +
                       theme(legend.title=element_blank()) +
                       ggtitle("Number of ties per agent after 500 cycles") +
                       xlab(expression(beta)) +
                       ylab(expression(alpha))
links.ties

ggsave(filename="tile_links_g4.pdf")

###############################################
### bar graphs of ties for 4 firm types

for (a in alpha.df) {
    for (b in beta.df) {
        title <- paste("Number of ties  (alpha = ", a, " beta = ", b,")")
        data <- subset(num.ties.data.g4, alpha == a & beta == b)
        alliance.histogram.g4 <- ggplot(data, aes(x=firm.type, y=link.count)) +
            geom_bar(stat="identity") +
            ylab("Number of ties") +
            xlab("Firm types") +
            expand_limits(y=c(0, 10000)) +
            scale_y_continuous(breaks=seq(0, 10000, 3000)) +
            ggtitle(title)
        alliance.histogram.g4

        fname <- paste("histogram_ties_g4_alpha_", a, "_beta_", b, ".pdf", sep="")
        ggsave(filename=fname)
    }
}

###############################################
### trellis graph number of ties for 4 firm types
alliance.hist.g4.trellis <- ggplot(num.ties.data.g4, aes(x=firm.type, y=link.count)) +
                                   geom_bar(stat="identity") +
                                   facet_grid(alpha ~ beta, as.table=FALSE) +
                                   ylab("Number of ties") +
                                   xlab("Firm types") +
                                   expand_limits(y=c(0, 10000)) +
                                   scale_y_continuous(breaks=seq(0, 10000, 3000)) 
alliance.hist.g4.trellis

ggsave('./alliance_hist_g4_trellis.pdf')

#######################################################
## number of links for each type of firms(I, II, III, IV), in a cycle
# trellis

max(num.ties.data.g4$link.count)

cyclic.num.ties.g4.trellis <- ggplot(num.ties.data.g4, 
                               aes(x=cycle, y=link.count,
                                   group=firm.type, colour=factor(firm.type))) +
                              geom_smooth() +
                              facet_grid(alpha ~ beta, as.table = FALSE) +
                              expand_limits(y=c(0,30)) +
                              scale_y_continuous("number of ties", breaks=seq(0,30,5)) +
                              scale_x_continuous("cycle") +
                              theme(legend.title=element_blank())
cyclic.num.ties.g4.trellis
        
ggsave('./cyclic_num_ties_g4_trellis.pdf')

######################### inter-firm ##########
###############################################
### bar graphs of inter-firm type ties

max(num.ties.data.inter.firm$tie.count)

for (a in alpha.df) {
    for (b in beta.df) {
        title <- paste("Number of inter-firm type ties  (alpha = ", a, " beta = ", b,")")
        data <- subset(num.ties.data.inter.firm, alpha == a & beta == b)

        alliance.histogram <- ggplot(data, aes(x=interfirm.tie.type, y=tie.count)) +
            geom_bar(stat="identity") +
            ylab("Number of ties") +
            xlab("Inter-firm types") +
            coord_flip() +
            expand_limits(y=c(0, 5000)) +
            scale_y_continuous(breaks=seq(0, 5000, 500)) +
            ggtitle(title)
        alliance.histogram

        fname <- paste("histogram_ties_g4_alpha_", a, "_beta_", b, ".pdf", sep="")
        ggsave(filename=fname)
    }
}

###############################################
### trellis graph interfirm number of ties

alliance.hist.inter.firm.trellis <- ggplot(num.ties.data.inter.firm, aes(x=interfirm.tie.type, y=tie.count)) +
                                           geom_bar(stat="identity") +
                                           facet_grid(alpha ~ beta, as.table=FALSE) +
                                           coord_flip() +
                                           ylab("Number of ties") +
                                           xlab("Inter-firm link types") +
                                           expand_limits(y=c(0, 4000)) +
                                           scale_y_continuous(breaks=seq(0, 4000, 1000))
alliance.hist.inter.firm.trellis

ggsave('./alliance_hist_inter_firm_trellis.pdf')

#######################################################
## number of interfirm type links, in a cycle

max(num.ties.data.inter.firm$tie.count)

cyclic.num.ties.interfirm.trellis <- ggplot(num.ties.data.inter.firm, 
                               aes(x=cycle, y=tie.count,
                                   group=interfirm.tie.type, colour=factor(interfirm.tie.type))) +
                              geom_smooth() +
                              facet_grid(alpha ~ beta, as.table = FALSE) +
                              expand_limits(y=c(0,9)) +
                              scale_y_continuous("number of links", breaks=seq(0,9,3)) +
                              scale_x_continuous("cycle") +
                              theme(legend.title=element_blank())
cyclic.num.ties.interfirm.trellis
        
ggsave('./cyclic_num_ties_interfirm_trellis.pdf')

##########################################################################
#-------------------   igraph network calc  ------------------------------
##########################################################################

## a data frame to create all 100 agents.
agents <- data.frame(c(seq(0,99)))
network.results.run.data <- data.frame()

if (file.exists('./network_results_run_data.txt')) {
    network.results.run.data <- dget('./network_results_run_data.txt')
} else {
      for (a in alpha.df) {
          for (b in beta.df) {
              for (r in run.df) {
                  for (c in cycle.seq.10) {
                      control <- c(a, b, r, c)
                      print(control)
                      ## obtain the subset for a definite cycle and run
                      analyzed.net.subset <- subset(agent.alliance.data, alpha == a &
                                                                         beta == b &
                                                                         cycle <= c &
                                                                         run == r )
                      ## beautify the list
                      rownames(analyzed.net.subset) <- NULL
                      keeps <- c("agent.id.1", "agent.id.2")
                
                      g <- graph.data.frame(analyzed.net.subset[keeps], directed=FALSE, vertices=agents)

                      ## DENSITY
                      g.density <- edge_density(g, loops = FALSE)
                      ## CLUSTER
                      g.cluster.num <- no.clusters(g)
                      ## CLUSTERING COEFFICIENT
                      g.clustering.coef <- transitivity(g, type="global")
                      ## DIAMETER
                      g.diameter <- diameter(g, directed=FALSE, unconnected=TRUE, weights=NULL)
                      ## CENTRALIZATION
                      g.centralization <- centralization.degree(g, mode="all")$centralization
                      g.closeness <- centralization.closeness(g, mode="all")$centralization
                      g.betweenness <- centralization.betweenness(g, directed=FALSE)$centralization

                      network.cycle.data <- c(r, c, a, b, g.density, g.cluster.num, g.clustering.coef,
                                              g.diameter, g.centralization, g.closeness, g.betweenness)
                      network.results.run.data <- rbind(network.results.run.data, network.cycle.data)
                  } # cycle
              } # run
          } # beta
      } # alpha
      names(network.results.run.data) <- c("run", "cycle", "alpha", "beta", "g.density",
                                           "g.cluster.num", "g.clustering.coef", "g.diameter",
                                           "g.centralization", "g.closeness", "g.betweenness")
      dput(network.results.run.data, file='./network_results_run_data.txt')
}

## create the data frame which have average network calculation values for all runs for each cycle.
network.results.data <- data.frame()

for (a in alpha.df) {
    for (b in beta.df) {
        for (c in cycle.seq.10) {
            ## obtain the subset for a definite cycle
            analyzed.subset <- subset(network.results.run.data, cycle==c &
                                                                alpha==a & beta==b)
            ## calculate the average of variables
            avg.g.density <- mean(analyzed.subset$g.density)
            avg.g.cluster.num <- mean(analyzed.subset$g.cluster.num)
            avg.g.clustering.coef <- mean(analyzed.subset$g.clustering.coef)
            avg.g.diameter <- mean(analyzed.subset$g.diameter)
            avg.g.centralization <- mean(analyzed.subset$g.centralization)
            avg.g.closeness <- mean(analyzed.subset$g.closeness)
            avg.g.betweenness <- mean(analyzed.subset$g.betweenness)

            ## create the data frame
            cycle.data <- data.frame(a, b, c, avg.g.density, avg.g.cluster.num,
                                     avg.g.clustering.coef, avg.g.diameter,
                                     avg.g.centralization, avg.g.closeness, avg.g.betweenness)
            ## insert the data vector to use in graphics
            network.results.data <- rbind(network.results.data, cycle.data)
        }
    }
}

names(network.results.data) <- c("alpha", "beta", "cycle", "avg.g.density", "avg.g.cluster.num",
                                 "avg.g.clustering.coef", "avg.g.diameter", "avg.g.centralization",
                                 "avg.g.closeness", "avg.g.betweenness")

network.results.set <- subset(network.results.data, cycle!=0)

##########################################################################

##########################################################################
### trellis graph of network values

## average graph density
max(network.results.data$avg.g.density)

avg.g.density.trellis <- ggplot(network.results.set, aes(x=cycle, y=avg.g.density)) +
                                geom_line() +
                                facet_grid(alpha ~ beta, as.table=FALSE) +
                                ylab("graph density") +
                                xlab("cycle") +
                                expand_limits(y=c(0, 6)) +
                                scale_y_continuous(breaks=seq(0, 6, 2))
avg.g.density.trellis

ggsave('./avg_g_density_trellis.pdf')

## average cluster num
max(network.results.set$avg.g.cluster.num)

avg.g.cluster.num.trellis <- ggplot(network.results.set, aes(x=cycle, y=avg.g.cluster.num)) +
                                    geom_line() +
                                    facet_grid(alpha ~ beta, as.table=FALSE) +
                                    ylab("number of cluster") +
                                    xlab("cycle") +
                                    expand_limits(y=c(0, 1.7)) +
                                    scale_y_continuous(breaks=seq(0, 1.7, 0.4))
avg.g.cluster.num.trellis

ggsave('./avg_g_cluster_num_trellis.pdf')

## avg cluster coef
max(network.results.set$avg.g.clustering.coef)

avg.g.clustering.coef.trellis <- ggplot(network.results.set, aes(x=cycle, y=avg.g.clustering.coef)) +
                                    geom_line() +
                                    facet_grid(alpha ~ beta, as.table=FALSE) +
                                    ylab("clustering coefficient") +
                                    xlab("cycle") +
                                    expand_limits(y=c(0, 0.7)) +
                                    scale_y_continuous(breaks=seq(0, 0.7, 0.2))
avg.g.clustering.coef.trellis

ggsave('./avg_g_clustering_coef_trellis.pdf')

## average diameter
max(network.results.set$avg.g.diameter)

avg.g.diameter.trellis <- ggplot(network.results.set, aes(x=cycle, y=avg.g.diameter)) +
                                           geom_line() +
                                           facet_grid(alpha ~ beta, as.table=FALSE) +
                                           ylab("network diameter") +
                                           xlab("cycle") +
                                           expand_limits(y=c(1.5, 7)) +
                                           scale_y_continuous(breaks=seq(0, 6, 2))
avg.g.diameter.trellis

ggsave('./avg_g_diameter_trellis.pdf')

## average centralization
max(network.results.set$avg.g.centralization)

avg.g.centralization.trellis <- ggplot(network.results.set, aes(x=cycle, y=avg.g.centralization)) +
                                           geom_line() +
                                           facet_grid(alpha ~ beta, as.table=FALSE) +
                                           ylab("centralization") +
                                           xlab("cycle") +
                                           expand_limits(y=c(0, 7.2)) +
                                           scale_y_continuous(breaks=seq(0, 6, 2))
avg.g.centralization.trellis

ggsave('./avg_g_centralization_trellis.pdf')

## average closeness
max(network.results.data$avg.g.closeness)

avg.g.closeness.trellis <- ggplot(network.results.data, aes(x=cycle, y=avg.g.closeness)) +
                                           geom_line() +
                                           facet_grid(alpha ~ beta, as.table=FALSE) +
                                           ylab("closeness") +
                                           xlab("cycle") +
                                           expand_limits(y=c(0, 0.3)) +
                                           scale_y_continuous(breaks=seq(0, 0.3, 0.1))
avg.g.closeness.trellis

ggsave('./avg_g_closeness_trellis.pdf')

## average betweenness
max(network.results.data$avg.g.betweenness)

avg.g.betweenness.trellis <- ggplot(network.results.data, aes(x=cycle, y=avg.g.betweenness)) +
                                           geom_line() +
                                           facet_grid(alpha ~ beta, as.table=FALSE) +
                                           ylab("betweenness") +
                                           xlab("cycle") +
                                           expand_limits(y=c(0, 0.05)) +
                                           scale_y_continuous(breaks=seq(0, 0.05, 0.01))
avg.g.betweenness.trellis

ggsave('./avg_g_betweenness_trellis.pdf')


###########################################
###########################################

## compare sapply(data_set, mode) to dget and loop results.

## to measure the memory usage.
gc()
object.size(x=lapply(ls(), get))
print(object.size(x=lapply(ls(), get)), units="MB")



