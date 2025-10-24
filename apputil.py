import pandas as pd


class GroupEstimate(object):
    def __init__(self, estimate):
        # ensure estimate is either "mean" or "median"
        if estimate not in ["mean", "median"]:
            raise ValueError("estimate must be either 'mean' or 'median'")
        self.estimate = estimate
    
    def fit(self, X, y):
        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be a pandas DataFrame.")
        if len(X) != len(y):
            raise ValueError("X and y must have the same length.")
        if pd.Series(y).isna().any():
            raise ValueError("y contains missing values.")
        
        # merge X and y
        df = X.copy()
        df["_target"] = y

        # group by all columns in X
        agg_func = "mean" if self.estimate == "mean" else "median"
        grouped = df.groupby(list(X.columns), dropna=False)["_target"].agg(agg_func)

        self._group_stats = grouped
        self._columns = list(X.columns)

        return self

    def predict(self, X):
        return None