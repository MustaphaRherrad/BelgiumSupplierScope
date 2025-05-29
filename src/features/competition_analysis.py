import pandas as pd

def calculate_competition_metrics(df):
    """Calcule les métriques de base de concurrence"""
    metrics = {
        'avg_bids_per_tender': df['tender_recordedbidscount'].mean(),
        'single_bidding_rate': (df.groupby('tender_id')['bid_id']
                               .transform('count') == 1).mean(),
        'unique_suppliers_count': df['bidder_id'].nunique()
    }
    return metrics

def calculate_hhi(df, group_col='tender_maincpv'):
    """Calcule l'indice Herfindahl-Hirschman par groupe"""
    def hhi(group):
        market_shares = group['bid_price'] / group['bid_price'].sum()
        return (market_shares**2).sum() * 10000
    
    return df.groupby(group_col).apply(hhi).reset_index(name='hhi_index')

def calculate_pareto(df):
    """Analyse Pareto des fournisseurs"""
    supplier_share = df.groupby('bidder_name')['bid_price'].sum().sort_values(ascending=False)
    supplier_share = supplier_share.reset_index()
    supplier_share['cum_pct'] = (supplier_share['bid_price'].cumsum() / 
                                supplier_share['bid_price'].sum()) * 100
    return supplier_share