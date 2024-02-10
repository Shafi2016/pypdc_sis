
def PDC_SIS(X, Y, lags=3, top_n=10):
    n, d = X.shape
    
    # Dynamically generate lagged versions of Y based on the specified 'lags'
    laggedYs = [np.roll(Y, lag) for lag in range(lags + 1)]
    for lag in range(1, lags + 1):
        laggedYs[lag][:lag] = np.nan  # Introducing NA for shifted parts
    
    # Combine all lagged versions of Y for conditioning
    Y_conditioning = np.column_stack(laggedYs)
    
    # Remove rows with NA values
    valid_rows = ~np.isnan(Y_conditioning).any(axis=1)
    Y_conditioning = Y_conditioning[valid_rows]
    X = X[valid_rows]
    
    # Reinitialize a vector for storing PDC values
    pdc = np.zeros(d)
    for j in range(d):
        # Compute PDC using the updated X and Y_conditioning without NAs
        pdc[j] = dcor.partial_distance_correlation(Y_conditioning[:, 0], X[:, j], Y_conditioning[:, 1:])
    
    # Determine top predictors based on PDC values
    indices = np.argsort(-np.abs(pdc))[:min(top_n, len(pdc))]
    
    return {
        'indices': indices,
        'screened_set': X[:, indices],
        'Y_conditioning_df': pd.DataFrame(Y_conditioning, columns=['Y'] + [f'Lag{i}' for i in range(1, lags + 1)])
    }