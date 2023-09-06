from shiny import App, render, ui, reactive
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotnine import *

app_ui = ui.page_fluid(

    ui.HTML(
        '''</head>
        <body>
        <center>
        <h2>Present Value of Cashflows by Coupon</h2>
        </center>
        <p></p>'''
    ),

    ui.panel_well(
        ui.input_slider("par", label="Bond Par", value=100, min=0, max = 150),
        ui.input_slider("discount", label="Discount Rate", min=1, max = 20, value = 3)
    ),

    ui.row(
        ui.column(6,ui.output_plot("grph", height='320px')),
        ui.column(6, ui.output_table("tbl"))
    )
)

def server(input, output, session):
    @reactive.Calc
    def calc():
        r = input.discount() / 100
        par = input.par()
        v = [1,2,3,4,5]
        df = pd.DataFrame(data = dict.fromkeys(v, v), index=v)
        df = df.apply(lambda x:  (par * (x.name/100)) / (1 + r) ** x.index)
        df.loc[5] = ((df.columns/100) * par + par) / (1 + r) ** 5
        df.loc[6] = df.sum(axis = 0)
        df = df.round(2)
        df['CF Year'] = [1,2,3,4,5,'PV']
        df = df[['CF Year', 1,2,3,4,5]]
        return df
      
    @output
    @render.plot
    def grph():
        df2 = calc().tail(1)
        df2 = df2[[1,2,3,4,5]].T
        df2.columns = ['PV']
         
        p = (ggplot(df2, aes(x=[1,2,3,4,5], y='PV'))
            + geom_col()
            + geom_hline(yintercept=100, linetype='dotted', color='blue', size=1.5)
            + annotate('label', x=5, y=input.par(), label=f'Par:{input.par()}', color='#770d50', size=8, label_size=0.2)
            + theme_bw()
            + labs(
                x = 'Coupon',
                y = 'PV',
                title = 'Present Value by Coupon')
        )

        return p

    @output 
    @render.table
    def tbl(): 
        return calc()
        
app = App(app_ui, server)    
