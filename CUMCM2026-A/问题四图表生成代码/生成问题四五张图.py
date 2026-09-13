# -*- coding: utf-8 -*-
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parent / 'data'
OUT=Path(__file__).resolve().parent / 'figures'
OUT.mkdir(parents=True,exist_ok=True)
z=np.load(ROOT/'plot_data.npz')
for fp in [r'C:\Windows\Fonts\simsun.ttc',r'C:\Windows\Fonts\consola.ttf']:
    if Path(fp).exists(): fm.fontManager.addfont(fp)
plt.rcParams.update({'font.family':['Consolas','SimSun'],'axes.unicode_minus':False,'font.size':12,'axes.titlesize':15,'axes.labelsize':12,'legend.fontsize':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':150})
BLUE='#1f5f8b'; ORANGE='#c26735'; GREEN='#2e8b78'; PURPLE='#7557a6'; GRID='#d8e0e5'
def save(fig,name):
    fig.tight_layout(); fig.savefig(OUT/name,dpi=300,bbox_inches='tight'); plt.close(fig)

# 图7-1: text values from 问题四(3).txt
N=np.array([400,800,1600]); td=np.array([51.107705,51.092627,51.088949])
fig,ax=plt.subplots(figsize=(6.8,4.3)); ax.plot(N,td,'o-',color=BLUE,lw=2,ms=7,mfc='white',mew=1.8)
for x,y in zip(N,td): ax.annotate(f'{y:.4f}',(x,y),xytext=(0,10),textcoords='offset points',ha='center',color=BLUE)
ax.set(xlabel='网格数 N',ylabel='预测烘干时间 / h',title='图7-1  烘干时间网格收敛曲线'); ax.set_xticks(N); ax.grid(alpha=.3); save(fig,'图7-1 烘干时间网格收敛曲线.png')

# 图7-2: radius history and PCHIP curve
r=z['radius_input']; t_in=r[:,0]/3600; R_in=r[:,1]; tt=z['q4_time_s']/3600; RR=z['q4_radius_cm']
fig,ax=plt.subplots(figsize=(7,4.4)); ax.plot(tt,RR,color=BLUE,lw=2,label='PCHIP 插值'); ax.scatter(t_in,R_in,s=12,color=ORANGE,alpha=.8,label='附件2观测点',zorder=3)
ax.set(xlabel='时间 / h',ylabel='半径 R / cm',title='图7-2  药材半径随时间变化'); ax.set_xlim(0,72); ax.set_ylim(1.15,2.05); ax.grid(alpha=.3); ax.legend(frameon=False); save(fig,'图7-2 药材半径随时间变化.png')

# 图7-3: table 7-2 radial profiles (physical distance)
pt=np.array([6,12,18,24,30,36,42,48,51.0889])
Rtab=np.array([1.374,1.248,1.214,1.204,1.201,1.200,1.200,1.200,1.200])
ct=np.array([[1.7188,1.5370,1.0222,.4205],[.7374,.6544,.4082,.1669],[.4086,.3686,.2397,.0892],[.2851,.2610,.1790,.0673],[.2263,.2094,.1493,.0595],[.1928,.1796,.1317,.0560],[.1712,.1604,.1200,.0541],[.1561,.1468,.1116,.0530],[.1500,.1413,.1081,.0526]])
fig,ax=plt.subplots(figsize=(7.4,4.8)); colors=plt.cm.viridis(np.linspace(.05,.92,len(pt)))
for i,(h,R,vals) in enumerate(zip(pt,Rtab,ct)):
    # anchors at center, 0.5 cm, 1 cm and surface; PCHIP gives smooth monotone profile
    xa=np.array([0,.5,1.0,R]); ya=vals
    mask=np.r_[True,np.diff(xa)>1e-9]
    xx=np.linspace(0,R,240); yy=np.interp(xx,xa[mask],ya[mask])
    ax.plot(xx,yy,lw=1.8,color=colors[i],label=f'{h:g} h')
ax.axhline(.15,color='#555',ls='--',lw=1,label='阈值 0.15')
ax.set(xlabel='距药材中心距离 / cm',ylabel='水分浓度 / (kg/kg)',title='图7-3  不同时刻水分浓度径向分布'); ax.grid(alpha=.25); ax.legend(ncol=2,frameon=False,loc='upper right'); save(fig,'图7-3 不同时刻水分浓度径向分布.png')

# 图7-4: interpolation comparison using attachment 2 and stated double exponential fit
x=np.linspace(0,72,600); pchip=PchipInterpolator(t_in,R_in,extrapolate=False); rp=np.where(x<=t_in[-1],pchip(x),R_in[-1]); rl=np.interp(x,t_in,R_in,left=R_in[0],right=R_in[-1]); rd=1.1999+0.1642*np.exp(-x/1.11)+0.6360*np.exp(-x/4.66)
fig,ax=plt.subplots(figsize=(7,4.4)); ax.plot(x,rp,color=BLUE,lw=2,label='PCHIP'); ax.plot(x,rl,color=ORANGE,lw=1.8,ls='--',label='线性插值'); ax.plot(x,rd,color=GREEN,lw=1.8,ls='-.',label='双指数拟合'); ax.scatter(t_in,R_in,s=10,color='k',alpha=.35,label='附件2观测点'); ax.set(xlabel='时间 / h',ylabel='半径 R / cm',title='图7-4  三种半径插值方法比较'); ax.set_xlim(0,72); ax.set_ylim(1.15,2.05); ax.grid(alpha=.3); ax.legend(frameon=False); save(fig,'半径插值方法比较.png')

# 图7-5: text values from table 7-5
methods=['PCHIP','线性插值','双指数拟合']; vals=[51.0889,51.0925,51.0733]
fig,ax=plt.subplots(figsize=(6.4,4.3)); bars=ax.bar(methods,vals,color=[BLUE,ORANGE,GREEN],width=.58); ax.set(ylabel='烘干时间 / h',title='图7-5  三种插值方法下的烘干时间对比'); ax.set_ylim(51.05,51.11); ax.grid(axis='y',alpha=.3)
for b,v in zip(bars,vals): ax.text(b.get_x()+b.get_width()/2,v+0.001,f'{v:.4f}',ha='center',va='bottom',fontsize=10)
save(fig,'烘干时间对比.png')
print('generated',*[p.name for p in OUT.glob('*.png') if p.name.startswith(('图7-','半径插值','烘干时间'))],sep='\n')
