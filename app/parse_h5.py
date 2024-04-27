import scanpy as sc
import pandas as pd
import redis_test as re
from tqdm import tqdm
import json

def normalize(df, group, n_groups=1, interval=20):
    largest_delta = 0
    largest_group = f"{group}0"

    for x in range(n_groups):
        print(x)
        min_value = df[f"{group}{x}"].min()
        max_value = df[f"{group}{x}"].max()
        delta = max_value - min_value
        print(delta)
        if delta > largest_delta:
            largest_delta = delta
            largest_group = f"{group}{x}"
        print(largest_delta)

    # Calculate the current min and max values of the global_sphere1 column
    min_value = df[largest_group].min()
    max_value = df[largest_group].max()

    print(largest_group)

    for x in range(n_groups):
        df[f'{group}{x}_norm'] = (df[f"{group}{x}"] - df[f"{group}{x}"].mean()) / (largest_delta/2)

    
def parse_h5(path):
    adata = sc.read(path)
    prefix = path.split('/')[-1].split('.')[0]

    # convert adata to df (normalized values)
    df = adata.to_df()
    # add the obs in the df
    df = pd.concat([df, adata.obs], axis=1)

    # add the brain projection coordinates in the df
    for x in range(adata.obsm["X_spatial"].shape[1]):
        df[f"X_spatial{x}"] = adata.obsm["X_spatial"][:,x]

    # add the umap coordinates in the df
    # iterate through all axis if there's more than 2, it accounts for it
    for x in range(adata.obsm["X_umap"].shape[1]):
        df[f"X_umap{x}"] = adata.obsm["X_umap"][:,x]

    normalize(df, "X_spatial", n_groups=adata.obsm["X_spatial"].shape[1])
    normalize(df, "X_umap", n_groups=adata.obsm["X_umap"].shape[1])


    # save to redis norm + obs + umap + spatial
    for col in tqdm(df):
        print(col)
        print()
        # re.save_to_redis(col, str(df[col].to_list()))
        re.save_to_redis(f"{prefix}-{col}", json.dumps(df[col].to_list()))
        # break

    # convert adata to df (raw values)
    df = pd.DataFrame(adata.obsm["X_raw"], columns=adata.to_df().columns, index=adata.obs.index)

    # save to redis raw
    for col in tqdm(df):
        re.save_to_redis(f"{prefix}-{col}_raw", json.dumps(df[col].to_list()))
        # break
    

    # # also save the uns for coloring purposes
    # re.save_to_redis("uns", str(adata.uns))
    # return df