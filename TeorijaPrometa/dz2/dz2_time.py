import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib
import matplotlib.pyplot as plt
import csv


matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')

#Funkcija za identifikaciju najbolje distribucije
def best_fit_distribution(data, bins=50, ax=None):
    # Histogram empirijskih podataka
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Popis svih distribucija - odaberite 5 ovisno o kakvim je podacima riječ
    '''
            
       
        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy

    

    
    DISTRIBUTIONS = [st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.genhalflogistic,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.hypsecant,st.invgamma,st.invgauss, 
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,
        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy,st.gilbrat,st.gengamma]
    '''
    DISTRIBUTIONS = [st.expon,st.norm, st.dweibull, st.reciprocal,st.halfgennorm,st.exponweib]

    # Varijable koje čuvaju najbolju distribuciju
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf
    

    # Procjena parametara distribucij
    for distribution in DISTRIBUTIONS:
        # Usporedba distribucija s empirijskih podatcima
        try:
            #Ignoriranje upozorenja
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # Identifikacija parametara distribucije
                params = distribution.fit(data)

                # Razdvajanje argumenata u pojedine parametre
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Izračun funkcije gustoće razdiobe te izračun sume kvadratne greške
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))
                                
                  
                # Dodavanje PDF-a na graf
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                except Exception:
                    pass

                # Provjera je li to najbolja distribucija
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params)

#Funkcija za iscrtavanje funkcije gustoće vjerojatnosti najbolje razdiobe
def make_pdf(dist, params, size=100):


    # Razdvajanje argumenata u pojedine parametre
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Identifikacija počektai kraja iscrtavanja razdiobe
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)
    end=1500
    # Generiranje podataka za iscrtavanje funkcije gustoće vjerojatnosti identificirane razdiobe
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf


#Učitavanje podataka iz datoteke
data_array=[]
with open('/home/filip/code/TeorijaPrometa/dz2/youtube_time.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter='\n')
        before = 2.027432
        i = 0
        for row in csvReader:
            time = float(row[0])
            if (time - before) * 1000 < 5: 
                data_array.append((time - before) * 1000)
            before = time
            i += 1
            if i > 5000:
                break

data = pd.Series(data=data_array)

# Prvi graf - histogram
plt.figure(figsize=(12,8))
ax = data.plot(kind='hist', bins=50, alpha=0.5)
#Postavljanje imena grafa te pojedine osi
ax.set_title('Histogram')
#ax.set_xlabel('Velicina paketa')
ax.set_xlabel('Međudolazno vrijeme')
ax.set_ylabel('Frekvencija pojavljivanja')

#Čuvanje veličine grafa za kasnije grafove
plt.figure(figsize=(12,8))
dataYLim = ax.get_ylim()


#Drugi graf - histogram sa funkcijama gustoće vjerojatnosti za sve razmatrane razdiobe
ax2 = data.plot(kind='hist', bins=50,  alpha=0.5)
# Pronalazak najbolje distribucije
best_fit_name, best_fit_params = best_fit_distribution(data, 500, ax2)
best_dist = getattr(st, best_fit_name)

plt.figure(figsize=(12,8))
ax2.set_ylim(dataYLim)
ax2.set_title('Histogram sa svim testiranim distribucijama')
#ax2.set_xlabel('Veličina paketa')
ax.set_xlabel('Međudolazno vrijeme')
ax2.set_ylabel('Frekvenica pojavljivanja')


# Izračun funkcije gustoće vjerojatnosti za najbolju razdiobu
pdf = make_pdf(best_dist, best_fit_params)
# Iscrtavanje trećeg grafa - histogram s funkcijom gustoće vjerojatnosti razdiobe koja najbolje opisuje empirijske podatke
ax3 = pdf.plot(lw=2, label='PDF', legend=True)
data.plot(kind='hist', bins=50, alpha=0.5, label='Data', legend=True, ax=ax3)
#Dodavanje parametara distribucije u poseban string za ispis na grafu
param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])
dist_str = '{}({})'.format(best_fit_name, param_str)

ax3.set_ylim(dataYLim)
ax3.set_title('Histogram sa najboljom distribucijama \n' + dist_str)
#ax3.set_xlabel('Veličina paketa')
ax.set_xlabel('Međudolazno vrijeme')
ax3.set_ylabel('Frekvenica pojavljivanja')
plt.show()