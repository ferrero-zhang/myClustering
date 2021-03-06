import basicClusterMethods as bcm
import dataSetPreprocessing as dp
import ensemble_generation as eg
import generate_constraints_link as gcl
import cop_kmeans as ck



#dataSets = {'digit': dp.loadDigits, 'movement': dp.loadMovement_libras}
#dataSets = {'digit': dp.loadDigits, 'movement': dp.loadMovement_libras, 'robot_1': dp.loadRobotExecution_1,
#            'robot_2': dp.loadRobotExecution_2, 'robot_4': dp.loadRobotExecution_4, 'synthetic': dp.loadSynthetic_control}

#commonParm = {'members': 20, 'classNum': 10, 'small_Clusters': 20, 'large_Clusters': 200, 'FSR': 1, 'SSR': 0.7}

#paramSettings = {'digit': commonParm,
#                 'movement': commonParm}

#eg.autoGenerationWithConsensus(dataSets, paramSettings)

dataSet, target = dp.loadIris()
must_link, cannot_link = gcl.generateConstraints(target, 2)
cluster, centers = ck.cop_KMeans(dataSet, 3, must_link, cannot_link)
print centers