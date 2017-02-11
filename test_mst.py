from MSTClustering import MSTClustering
import numpy as np
import os
import cluster_visualization as cv


def mst_with_cutoff(distance_matrix, pos, savepath, cutoff_type='rate',
                    cutoff_upper=0.9, cutoff_lower=0.1, interval=0.05):
    """
    Do several MST clustering on given library of solutions in a range of different 'cutoff' parameters
    Used for deciding the suitable cutoff value which will be utilized in the MST selection procedure

    Parameters
    ----------
    :param distance_matrix: distance matrix of given library of solutions
    :param pos: positions generated by MDS or other embedding approaches, used for visualization
    :param savepath: path where the visualization of clustering result stored
    :param cutoff_type: type of parameter 'cutoff', should either be :
                       'threshold' :  edges with larger weight than threshold will be cut
                       'rate' :       number(>=1) / fraction(<1.0) of edges that will be cut
    :param cutoff_upper: upper bound of parameter cutoff
    :param cutoff_lower: lower bound of parameter cutoff
    :param interval: interval of parameter cutoff

    """
    # do MST clustering by setting 'cutoff' between [cutoff_lower, cutoff_upper] with given interval
    cur_cutoff = cutoff_lower
    while cur_cutoff <= cutoff_upper:
        if cutoff_type == 'threshold':
            mstmodel = MSTClustering(cutoff_scale=cur_cutoff, min_cluster_size=2,
                                     metric='precomputed', approximate=False)
        else:
            mstmodel = MSTClustering(cutoff=cur_cutoff, min_cluster_size=2,
                                     metric='precomputed', approximate=False)
        mstmodel.fit(distance_matrix[0:-5, 0:-5])
        filename = savepath + str(cur_cutoff) + '.png'
        cv.plot_mst_result(mstmodel, pos, filename)
        cur_cutoff += interval
    return


def mst_with_cutoff_in_folder(nidpath, pospath, savepath, distype='nid', cutoff_type='rate',
                    cutoff_upper=0.9, cutoff_lower=0.1, interval=0.05):
    """
    Do MST clustering on all library of solutions in given directory with specific parameters

    Parameters
    ----------
    :param nidpath: path where distance matrix stored
    :param pospath: path where positions stored
    :param savepath: path where the visualizations of clustering result stored
    :param distype: type of distance used
    :param cutoff_type: type of parameter 'cutoff', should either be :
                       'threshold' :  edges with larger weight than threshold will be cut
                       'rate' :       number(>=1) / fraction(<1.0) of edges that will be cut
    :param cutoff_upper: upper bound of parameter cutoff
    :param cutoff_lower: lower bound of parameter cutoff
    :param interval: interval of parameter cutoff

    """
    if not os.path.isdir(savepath):
        os.mkdir(savepath)
    nidpath = os.path.expanduser(nidpath)
    for f in os.listdir(nidpath):
        # deal with macOS's '.DS_Store'
        if f.startswith('.'):
            continue
        if distype not in f:
            continue
        fullpath = os.path.join(nidpath, f)
        if os.path.isfile(fullpath):
            fname = os.path.splitext(f)
            filename = fname[0].split('_' + distype)[0]
            dataset_name = filename.split('_')[0]
            if not os.path.isdir(savepath + dataset_name):
                os.mkdir(savepath + dataset_name)

            # read distances and positions
            distance_matrix = np.loadtxt(fullpath, delimiter=',')
            pos = np.loadtxt(pospath + filename + '_mds2d.txt', delimiter=',')
            det_savepath = savepath + dataset_name + '/' + filename + '_afterMST' + '_'

            mst_with_cutoff(distance_matrix, pos, det_savepath, cutoff_type=cutoff_type, cutoff_lower=cutoff_lower,
                            cutoff_upper=cutoff_upper, interval=interval)
    return
