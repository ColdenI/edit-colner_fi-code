def screen_normalization(screen_resolution):
    stat_= (1600,900)
    nX=stat_[0] / screen_resolution[0]
    nY=stat_[1] / screen_resolution[1]
    return (nX,nY)