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
        if not hasattr(self, "_group_stats") or not hasattr(self, "_columns"):
            raise RuntimeError("Model is not fitted yet. Call fit(X, y) first.")

        # normalize input to DataFrame with training columns
        if isinstance(X, pd.DataFrame):
            X_new = X[self._columns].copy()
        else:
            # allow single row like ["Brazil","Light"] or multiple rows
            if isinstance(X, (list, tuple)) and X and not isinstance(X[0], (list, tuple, pd.Series, dict)):
                X = [X]
            X_new = pd.DataFrame(X, columns=self._columns)

        # left-join with learned group stats
        stats = self._group_stats.reset_index().rename(columns={"_target": "estimate"})
        merged = X_new.merge(stats, how="left", on=self._columns)
        preds = merged["estimate"]

        # report missing combos
        missing = int(preds.isna().sum())
        if missing > 0:
            print(f"[GroupEstimate.predict] {missing} observation(s) had unseen category combinations; returning NaN.")

        return preds.to_numpy()