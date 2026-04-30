import pandas as pd
import numpy as np
from tabulate import tabulate
import statistics

class Descriptive:
    def pdread(self, pfname, **kwargs):
        """Read CSV with additional options"""
        return pd.read_csv(pfname, header=0, **kwargs)
    
    def analysis(self, pdf, numeric_only=True):
        """Generate descriptive statistics"""
        if numeric_only:
            pdf = pdf.select_dtypes(include=[np.number])
        
        stats = pd.DataFrame({
            'Count': pdf.count(),
            'Min': pdf.min(),
            'Max': pdf.max(),
            'Mean': pdf.mean(),
            'Std': pdf.std(),
            '25%': pdf.quantile(0.25),
            '50%': pdf.quantile(0.50),
            '75%': pdf.quantile(0.75)
        }).T
        return stats
    
    def dataanalysis(self, idf):
        colom_name=idf.columns
        df = pandas.DataFrame({'status':{
                                        1:'Count',
                                        2:'Min',
                                        3:'Max',
                                        4:'Mean',
                                        5:'Fmean',
                                        6:'Geometric Mean',
                                        #7:'Harmonic Mean',
                                        8:'Median',
                                        9:'Median Low',
                                        10:'Median High',
                                        11:'Median Grouped',
                                        12:'Mode',
                                        13:'Multimode',
                                        14:'Quantiles(0.25)',
                                        15:'Quantiles(0.75)',
                                        16:'Population standard deviation',
                                        17:'Population variance',
                                        18:'Sample standard deviation',
                                        19:'Sample variance',
                                        #20:'Skewness',
                                        #21:'kurtosis',
                                        #22:'The standard error of the mean',
                                        #23:'Tie correction factor',
                                        #24:'one-way chi-square test (statistic,pvalue)',
                                        #25:'Shapiro-Wilk test (statistic,pvalue)',
                                        #26:'Wilcoxon signed-rank test (statistic,pvalue)'
                                        }
                                })
        for cn in colom_name:
            try:
                gmean=statistics.geometric_mean(idf[cn])
            except ValueError:
                gmean='none'

            df[cn]={
                1:len(idf[cn]),
                2:min(idf[cn]),
                3:max(idf[cn]),
                4:statistics.mean(idf[cn]),
                5:statistics.fmean(idf[cn]),
                6:gmean,
                #7:statistics.harmonic_mean(idf[cn]),
                8:statistics.median(idf[cn]),
                9:statistics.median_low(idf[cn]),
                10:statistics.median_high(idf[cn]),
                11:statistics.median_grouped(idf[cn]),
                12:statistics.mode(idf[cn]),
                13:statistics.multimode(idf[cn]),
                14:statistics.quantiles(idf[cn])[0],
                15:statistics.quantiles(idf[cn])[2],
                16:statistics.pstdev(idf[cn]),
                17:statistics.pvariance(idf[cn]),
                18:statistics.stdev(idf[cn]),
                19:statistics.variance(idf[cn]),
                
                #20:scipy.stats.skew(idf[cn],axis=0, bias=True),
                #21:scipy.stats.kurtosis(idf[cn],axis=0, bias=True),
                #22:scipy.stats.sem(idf[cn],axis=None, ddof=0),
                #23:scipy.stats.tiecorrect(scipy.stats.rankdata(idf[cn])),
                #24:scipy.stats.chisquare(idf[cn]),
                #25:scipy.stats.shapiro(idf[cn]),
                #26:scipy.stats.wilcoxon(idf[cn]),
            }
        return tabulate(df, headers='keys', tablefmt='grid', floatfmt='.2f')