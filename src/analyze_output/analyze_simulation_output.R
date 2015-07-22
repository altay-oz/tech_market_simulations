# this file analyzes the output of simulations carried out under
# different alpha and beta values
# http://igraph.org/c/doc/igraph-Structural.html
library(igraph)
library(ggplot2)

# list all directories

setwd("../..")

output_directories <- dir(pattern = "^output_")


# ----------------------------------------------------------------------
# create empty matrices
# analysis 1
# create an empty data matrix for learning, cumulative knowledge etc.
learning_knowledge_data <- matrix(, ncol=6)

# analysis 2 - 3
# create an empty matrix for the number of ties
num_ties_data <- matrix(, ncol=7)
num_ties_inter_type_data <- matrix(, ncol=13)

# analysis 4
# create an empty matrix for the network analysis results
network_results_data <- matrix(, ncol=11)

################################################
# load all data frames
for (output_dir in output_directories) {
    setwd(output_dir)
################################################
    
    # use this if you don't use the loop and the two lines above
    setwd("../../output_alpha_0.05_beta_2.0")

    # get the alpha and beta values
    alpha_beta <- read.csv(file="alpha_beta_file.txt", head=FALSE, sep=",")
    alpha <- alpha_beta[,1]
    beta <- alpha_beta[,2]
    
    # load all data in the directory
    agent_cycle_orj <- read.csv(file="data_agent_cycle.txt", head=TRUE, sep=",")
    agent_orj <- read.csv(file="data_agent.txt", head=TRUE, sep=",")
    agent_alliance_orj <- read.csv(file="data_alliance.txt", head=TRUE, sep=",")
    network_data_orj <- read.csv(file="data_network.txt", head=TRUE, sep=",")

    # ---- ANALYZE NO 1 ----------
    # drawing accumulated knowledge v. cycle for 4 firm types
    # ---- agent -----------------
    # add firm_type. This depends on sigma_m and sigma_t. There are 4 types of firms.
    agent_orj$type[ agent_orj$sigma_m < 1.5 & agent_orj$sigma_k < 1.5 ]   <- 'I' 
    agent_orj$type[ agent_orj$sigma_m < 1.5 & agent_orj$sigma_k >= 1.5 ]  <- 'II'
    agent_orj$type[ agent_orj$sigma_m >= 1.5 & agent_orj$sigma_k >= 1.5 ] <- 'III'
    agent_orj$type[ agent_orj$sigma_m >= 1.5 & agent_orj$sigma_k < 1.5 ]  <- 'IV'

    # get a copy of the read data
    agent_cycle <- agent_cycle_orj
    # agents' places on the map, add two more columns
    agent_cycle$map_market <- NULL
    agent_cycle$map_knowledge <- NULL

    # get a copy of the data frame
    agent <- agent_orj
    agent$cycle <- NULL
    agent$entry_cycle <- NULL
    agent$sigma_m <- NULL
    agent$sigma_k <- NULL

    # agent_cyle + alpha + beta
    agent_cycle$alpha <- alpha
    agent_cycle$beta <- beta

    # with this we are adding agent and agent_cycle with a match btw. run and agent_id
    agent_cycle_type <- merge(agent_cycle, agent, by = c("run", "agent_id"))

    head(agent_cycle_type)
    
    # ---- ANALYZE NO 2 ----------------
    # ---- alliance --------------------
    alliances <- agent_alliance_orj

    # with this we are adding the firm type column for the two columns(dyadic network)
    agent_all_temp1 <- merge(alliances, agent, by.x = c("run", "agent_id1"), by.y = c("run", "agent_id"))
    colnames(agent_all_temp1)[5] <- c("type_1")
    agent_alliance <- merge(agent_all_temp1, agent, by.x = c("run", "agent_id2"), by.y = c("run", "agent_id"))
    colnames(agent_alliance)[6] <- c("type_2")
    
    # -----------------------------------
    # --- other variables ---------------
    # used in the loop bellow
    cycle_seq <- seq(0,500, by=10)
    run <- c(1:5)
    firm_type <- c("I","II","III","IV")
    
   # ---- ANALYZE 1 ----------------------------------------------------------------
    for (c in cycle_seq) {
        for (t in firm_type) {
            # obtain the subset for a definite cycle, firm_type
            analyzed_subset_1 <- subset(agent_cycle_type, cycle==c & type==t)
            # calculate the average of cumulated and cyclic knowledge
            avg_knowledge <- mean(analyzed_subset_1$cum_knowledge)
            avg_cyclic_learning <- mean(analyzed_subset_1$cycle_realized_learning)
            # create the data vector
            cycle_data_1 <- c(c, alpha, beta, t, avg_knowledge, avg_cyclic_learning)
            # insert the data vector for future use
            learning_knowledge_data <- rbind(learning_knowledge_data, cycle_data_1)
        }
    } # end ANALYZE 1

    # ---- ANALYZE 2, number of ties for each group. -------------------------------
    for (c in cycle_seq) {
        # obtain the subset for a definite cycle, firm_type
        analyzed_subset_2 <- subset(agent_alliance, cycle <= c)

        # the file contain both a-b and b-a ties thus counting only a single column is OK.
        count_firm_types <- table(analyzed_subset_2$type_1)

        # TODO
        type_1 <- count_firm_types[names(count_firm_types)=="I"]
        type_2 <- count_firm_types[names(count_firm_types)=="II"]
        type_3 <- count_firm_types[names(count_firm_types)=="III"]
        type_4 <- count_firm_types[names(count_firm_types)=="IV"]            

        # TODO
        if (length(count_firm_types) == 0) {
            type_1 <- 0
            type_2 <- 0
            type_3 <- 0
            type_4 <- 0
        }
        
        # the resulting data vector for this cycle
        cycle_data_2 <- c(c, alpha, beta, type_1, type_2, type_3, type_4)
        
        # insert the data vector for future use
        num_ties_data <- suppressWarnings(rbind(num_ties_data, cycle_data_2))

        # ---- ANALYZE 3, number of ties between groups.--------------------------------------
        # the number of ties within the same group is counted twice one from A to B
        # then from B to A as it is made for the ties made between different group firms.
        count_I_I <- nrow(subset(analyzed_subset_2, type_1 = "I", type_2 == "I")) / max(run)
        count_II_II <- nrow(subset(analyzed_subset_2, type_1 = "II", type_2 == "II")) / max(run)
        count_III_III <- nrow(subset(analyzed_subset_2, type_1 = "III", type_2 == "III")) / max(run)
        count_IV_IV <- nrow(subset(analyzed_subset_2, type_1 = "IV", type_2 == "IV")) / max(run)
        count_I_II   <- nrow(subset(analyzed_subset_2, type_1 = "I", type_2 == "II")) / max(run)
        count_I_III  <- nrow(subset(analyzed_subset_2, type_1 = "I", type_2 == "III")) / max(run)
        count_I_IV   <- nrow(subset(analyzed_subset_2, type_1 = "I", type_2 == "VI"))  / max(run)
        count_II_III <- nrow(subset(analyzed_subset_2, type_1 = "II", type_2 == "III")) / max(run)
        count_II_IV  <- nrow(subset(analyzed_subset_2, type_1 = "II", type_2 == "IV")) / max(run)
        count_III_IV <- nrow(subset(analyzed_subset_2, type_1 = "III", type_2 == "IV")) / max(run) 

        cycle_data_3 <- c(c, alpha, beta, count_I_I, count_II_II, count_III_III, count_IV_IV,
                        count_I_II, count_I_III, count_I_IV, count_II_III, count_II_IV,
                        count_III_IV)
        num_ties_inter_type_data <- rbind(num_ties_inter_type_data, cycle_data_3)

    } # end ANALYZE 2 and 3

    # number_of_possible_edges = (n-1)*n/2    [here n = 100]

    # ---- ANALYZE 4, network analysis  ------------------------------------------------
    for (c in cycle_seq) {
        for (r in run) {
            # obtain the subset for a definite cycle and run
            analyzed_subset_3 <- subset(agent_alliance, cycle<=c, run==r)
                        
            analyzed_subset_3$run <- NULL
            analyzed_subset_3$cycle <- NULL
            analyzed_subset_3$type_1 <- NULL
            analyzed_subset_3$type_2 <- NULL

            # remove all similar edges
            analyzed_subset_3 <- unique(analyzed_subset_3)
            # beautify the list
            rownames(analyzed_subset_3) <- NULL

            # create an empty graph
            g <- graph.empty() + vertices(c(1:100))
            # add edges to the empty graph
            if (length(analyzed_subset_3) > 0) {                
                g <- g + graph.data.frame(analyzed_subset_3)
            }
            # as there are paralel edges, we should simplify
            # log files take a and b, b and a simultaneously for the same link. 
            g <- as.undirected(g)
            g <- simplify(g)

            # DENSITY
            g_density <- graph.density(g, loops=FALSE)
            # CLUSTER
            g_cluster_num <- no.clusters(g)
            # CLUSTERING COEFFICIENT
            g_clustering_coef <- transitivity(g, type="global")
            # DIAMETER
            g_diameter <- diameter(g, directed=FALSE, unconnected=TRUE, weights=NULL)
            # CENTRALIZATION
            g_centralization <- centralization.degree(g, mode="all")$centralization
            g_closeness <- centralization.closeness(g, mode="all")$centralization
            g_betweenness <- centralization.betweenness(g, directed=FALSE)$centralization

            cycle_data_4 <- c(r, c, alpha, beta, g_density, g_cluster_num, g_clustering_coef,
                                      g_diameter, g_centralization, g_closeness, g_betweenness)
            network_results_data <- rbind(network_results_data, cycle_data_4)

################################################
        } # end run
    } # end ANALYZE 4
    setwd("../")
} # directories end of the loop
################################################

# ------ clean all -----------
# analysis 1
rownames(learning_knowledge_data) <- NULL
learning_knowledge_data <- learning_knowledge_data[-1,]
colnames(learning_knowledge_data) <- c("cycle", "alpha", "beta", "firm_type",
                                       "avg_knowledge", "avg_cyclic_learning")
learning_knowledge_data <- as.data.frame(learning_knowledge_data)
head(learning_knowledge_data)

learning_knowledge_data

# analysis 2 3
rownames(num_ties_data) <- NULL
num_ties_data <- num_ties_data[-1,]
colnames(num_ties_data) <- c("cycle", "alpha", "beta", "type_1", "type_2", "type_3", "type_4")
num_ties_data <- as.data.frame(num_ties_data)
head(num_ties_data)

#--

rownames(num_ties_inter_type_data) <- NULL
num_ties_inter_type_data <- num_ties_inter_type_data[-1,]
colnames(num_ties_inter_type_data) <- c("cycle", "alpha", "beta", "count_I_I", "count_II_II",
                                        "count_III_III", "count_IV_IV", "count_I_II", "count_I_III",
                                        "count_I_IV", "count_II_III", "count_II_IV", "count_III_IV")
num_ties_inter_type_data <- as.data.frame(num_ties_inter_type_data)
head(num_ties_inter_type_data)

# analysis 4
rownames(network_results_data) <- NULL
network_results_data <- network_results_data[-1,]
colnames(network_results_data) <- c("run", "cycle", "alpha", "beta", "density", "cluster_num",
                                    "clustering_coef", "diameter", "centralization",
                                    "closeness", "betweenness")
network_results_data <- as.data.frame(network_results_data)
head(network_results_data)



# --- CREATE GRAPHICS -------------------------------------------------------------
# --- for distinct alpha and beta -------

# --- A1 ------ learning, knowledge per cycle 
# learning_knowledge_data <- c(c, alpha, beta, t, avg_knowledge, avg_cyclic_learning)

# KALDI

learning_know_subset <- subset(learning_knowledge_data, cycle==500, select=-c(avg_cyclic_learning))
rownames(learning_know_subset) <- NULL
learning_know_subset <- subset(learning_know_subset, select=-c(cycle))

names(learning_know_subset)
head(learning_know_subset)

# obtain the alpha and beta unique values
a_list <- unique(learning_know_subset$alpha)
b_list <- unique(learning_know_subset$beta)

# create a list to be used in loop
a_list <- as.numeric(levels(droplevels(a_list)))
b_list <- as.numeric(levels(droplevels(b_list)))

ab_know_data <- data.frame(a=double(), b=double(), avg_know=double())

ab_know_data

for (a in a_list) {
    for (b in b_list) {
        avg_know_list <- learning_know_subset$avg_knowledge[learning_know_subset$alpha==a &
                                                            learning_know_subset$beta==b]
        avg_know_ok <- as.numeric(levels(droplevels(avg_know_list)))
        avg_know <- mean(avg_know_ok)
        ab_know_data <- rbind(ab_know_data, c(a, b, avg_know))
    }
}

colnames(ab_know_data) <- c("alpha", "beta", "avg_know")

ab_know_data

learning_total <- ggplot(ab_know_data, aes(x=beta, y=alpha)) +
                         geom_tile(aes(fill=avg_know)) +
                        theme(legend.title=element_blank()) +
                        ggtitle("Avg. accumulated knowledge") +
                        xlab(expression(beta)) +
                        ylab(expression(alpha))
learning_total

ggsave(filename="tile_learning_total.pdf")

title <- paste("Learning in a cycle, expression(alpha) =", alpha, "beta =", beta, sep=" ")

cyclic_learning <- ggplot(learning_knowledge_data,
                   aes(x=c, y=avg_cyclic_learning, group=t, colour=factor(t))) +
                    geom_line() +
                    ylab("learning") +
                    xlab("cycle") +
                   ggtitle("Learning in a cycle, expression(alpha) =  expression(beta) = ")
cyclic_learning
fname <- paste("learning_in_cycle_alpha_", alpha, "_beta_", beta, ".pdf", sep="")
ggsave(filename=fname)

title <- paste("Accumulated knowledge, alpha =", alpha, "beta =", beta, sep=" ")
avg_know <- ggplot(learning_knowledge_data,
                   aes(x=c, y=avg_knowledge, group=t, colour=factor(t))) +
                    geom_line() +
                    ylab("Accumulated knowledge") +
                    xlab("cycle") +
                   ggtitle(title)
avg_know
fname <- paste("avg_know_alpha_", alpha, "_beta_", beta, ".pdf", sep="")
ggsave(filename=fname)

# --- A2 ------ number of ties for each firm type (I, II, III, IV)
# num_ties_data <- c(c, alpha, beta, type_1, type_2, type_3, type_4)




# --- A3 ------ intergroup allince numbers
num_ties_inter_type_data <- c(c, alpha, beta, count_I_I, count_II_II, count_III_III, count_IV_IV,
                          count_I_II, count_I_III, count_I_IV, count_II_III, count_II_IV,
                          count_III_IV)

# --- A4 ------- network values over cycles

network_results_data <- c(c, alpha, beta, g_density, g_cluster_num, g_clustering_coef,
                          g_diameter, g_centralization, g_closeness, g_betweenness)
        



# --- CREATE OTHER GRAPHICS -------------------------------------------------------
# --- for _different_ alphas and betas on the same graph -------


#demo(package="igraph", centrality)
