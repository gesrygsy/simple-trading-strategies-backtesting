import matplotlib.pyplot as plt

def show_plt(data, data_dir, down_sampling, **kwargs):
    print('\nLoading plot...')
    param = {}

    for key, value in kwargs.items():
        param[key] = value
    dlen_f = abs(len(data) - 0)
    dlen_b = 0

    try:
        date = list(data['Datetime'])[dlen_b:dlen_f]
    except:
        date = data.index.values.tolist()[dlen_b:dlen_f]
    price = list(data['Open'])[dlen_b:dlen_f]

    if param['strategy'] == 'RSI':
        rsi = list(data[f"RSI{param['period']}"])[dlen_b:dlen_f]
    elif param['strategy'] == 'MFI':
        mfi = list(data[f"MFI{param['period']}"])[dlen_b:dlen_f]
    elif param['strategy'] == 'BBands':
        bbands_upper = list(data[f"BB_U_{param['period']}"])[dlen_b:dlen_f]
        bbands_middle = list(data[f"BB_M_{param['period']}"])[dlen_b:dlen_f]
        bbands_lower = list(data[f"BB_L_{param['period']}"])[dlen_b:dlen_f]
    elif param['strategy'] == 'Stoch':
        stoch_sk = list(data[f"S{param['fastk']}_slowk"])[dlen_b:dlen_f]
        stoch_sd = list(data[f"S{param['fastk']}_slowd"])[dlen_b:dlen_f]
    elif param['strategy'] == 'Stochf':
        stochf_fk = list(data[f"Sf{param['fastk']}_fastk"])[dlen_b:dlen_f]
        stochf_fd = list(data[f"Sf{param['fastd']}_fastd"])[dlen_b:dlen_f]
    elif param['strategy'] == 'StochRSI':
        stochrsi_fastk = list(data[f"SRSI{param['period']}_fastk"])[dlen_b:dlen_f]
        stochrsi_fastd = list(data[f"SRSI{param['period']}_fastd"])[dlen_b:dlen_f]
    elif param['strategy'] == 'MACD':
        macd = list(data[f"MACD_f{param['fastperiod']}_s{param['slowperiod']}_sig{param['signalperiod']}"])[dlen_b:dlen_f]
        macd_signal = list(data[f"MACDsignal_f{param['fastperiod']}_s{param['slowperiod']}_sig{param['signalperiod']}"])[dlen_b:dlen_f]
        macd_hist = list(data[f"MACDhist_f{param['fastperiod']}_s{param['slowperiod']}_sig{param['signalperiod']}"])[dlen_b:dlen_f]
    elif param['strategy'] == 'ROC':
        roc = list(data[f"ROC{param['period']}"])[dlen_b:dlen_f]
    elif param['strategy'] == 'ADX':
        adx = list(data[f"ADX{param['period']}"])[dlen_b:dlen_f]
    elif param['strategy'] == 'MOM':
        mom = list(data[f"MOM{param['period_mom']}"])[dlen_b:dlen_f]
        upper_mom = list(data["U_MOM"])[dlen_b:dlen_f]
        upper_mom_period = list(data["U_MOM_period"])[dlen_b:dlen_f]
        lower_mom = list(data["L_MOM"])[dlen_b:dlen_f]
        lower_mom_period = list(data["L_MOM_period"])[dlen_b:dlen_f]
    elif param['strategy'] == 'KAMA':
        kama = list(data[f"KAMA{param['period']}"])[dlen_b:dlen_f]
        cross = list(data['Cross'])[dlen_b:dlen_f]
        try:
            cross_tp = list(data['Cross_TP'])[dlen_b:dlen_f]
        except:
            pass
    elif param['strategy'] == 'Hilbert':
        # hilbert_period = list(data['Hil_Period'])[dlen_b:dlen_f]
        hilbert_phase = list(data['Phase'])[dlen_b:dlen_f]
        # hilbert_inphase = list(data['InPhase'])[dlen_b:dlen_f]
        # hilbert_quadrature = list(data['Quadrature'])[dlen_b:dlen_f]
        # hilbert_sine = list(data['Sine'])[dlen_b:dlen_f]
        # hilbert_leadsine = list(data['Leadsine'])[dlen_b:dlen_f]
        hilbert_integer = list(data['Integer'])[dlen_b:dlen_f]
    elif param['strategy'] == 'PPO':
        ppo = list(data['PPO'])[dlen_b:dlen_f]
        ppo_signal = list(data['PPO_Signal'])[dlen_b:dlen_f]
    elif param['strategy'] == 'Chaikin_AD':
        chaikin_ad = list(data[f"AD_f{param['fastperiod']}_s{param['slowperiod']}"])
    
    signal = list(data['Signal'])[dlen_b:dlen_f]
    aposition = list(data['aPosition'])[dlen_b:dlen_f]
    cum_pnl = list(data['Cum_PnL']/param['pip'])[dlen_b:dlen_f]
    
    try:
        ma = list(data[f"MA{param['period_ma']}"])[dlen_b:dlen_f]
        trend = list(data['Trend'])[dlen_b:dlen_f]
        signal_t = list(data['Signal_T'])[dlen_b:dlen_f]
    except:
        pass

    if down_sampling:
        div = 500
        date = date[::round((dlen_f - dlen_b) / div)]
        price = price[::round((dlen_f - dlen_b) / div)]
        signal = signal[::round((dlen_f - dlen_b) / div)]
        aposition = aposition[::round((dlen_f - dlen_b) / div)]
        cum_pnl = cum_pnl[::round((dlen_f - dlen_b) / div)]

        if param['strategy'] == 'RSI':
            rsi = rsi[::round((dlen_f - dlen_b) / div)]
        elif param['strategy'] == 'MFI':
            mfi = mfi[::round((dlen_f - dlen_b) / div)]
        elif param['strategy'] == 'BBands':
            bbands_upper = bbands_upper[::round((dlen_f - dlen_b) / div)]
            bbands_middle = bbands_middle[::round((dlen_f - dlen_b) / div)]
            bbands_lower = bbands_lower[::round((dlen_f - dlen_b) / div)]
        elif param['strategy'] == 'Stoch':
            stoch_sk = stoch_sk[::round((dlen_f - dlen_b) / div)]
            stoch_sd = stoch_sd[::round((dlen_f - dlen_b) / div)]
        elif param['strategy'] == 'Stochf':
            stochf_fk = stochf_fk[::round((dlen_f - dlen_b) / div)]
            stochf_fd = stochf_fd[::round((dlen_f - dlen_b) / div)]
        elif param['strategy'] == 'StochRSI':
            stochrsi_fastk = stochrsi_fastk[::round((dlen_f - dlen_b) / div)]
            stochrsi_fastd = stochrsi_fastd[::round((dlen_f - dlen_b) / div)]
        elif param['strategy'] == 'MACD':
            macd = macd[::round((dlen_f - dlen_b) / div)]
            macd_signal = macd_signal[::round((dlen_f - dlen_b) / div)]
            macd_hist = macd_hist[::round((dlen_f - dlen_b) / div)]
        elif param['strategy'] == 'ROC':
            roc = roc[::round((dlen_f - dlen_b) / div)]
        elif param['strategy'] == 'ADX':
            adx = adx[::round((dlen_f - dlen_b) / div)]
        elif param['strategy'] == 'MOM':
            mom = mom[::round((dlen_f - dlen_b) / div)]
            upper_mom = upper_mom[::round((dlen_f - dlen_b) / div)]
            upper_mom_period = upper_mom_period[::round((dlen_f - dlen_b) / div)]
            lower_mom = lower_mom[::round((dlen_f - dlen_b) / div)]
            lower_mom_period = lower_mom_period[::round((dlen_f - dlen_b) / div)]
        elif param['strategy'] == 'KAMA':
            kama = kama[::round((dlen_f - dlen_b) / div)]
            cross = cross[::round((dlen_f - dlen_b) / div)]
            try:
                cross_tp = cross_tp[::round((dlen_f - dlen_b) / div)]
            except:
                pass
        elif param['strategy'] == 'Hilbert':
            # hilbert_period = hilbert_period[::round((dlen_f - dlen_b) / div)]
            hilbert_phase = hilbert_phase[::round((dlen_f - dlen_b) / div)]
            # hilbert_inphase = hilbert_inphase[::round((dlen_f - dlen_b) / div)]
            # hilbert_quadrature = hilbert_quadrature[::round((dlen_f - dlen_b) / div)]
            # hilbert_sine = hilbert_sine[::round((dlen_f - dlen_b) / div)]
            # hilbert_leadsine = hilbert_leadsine[::round((dlen_f - dlen_b) / div)]
            hilbert_integer = hilbert_integer[::round((dlen_f - dlen_b) / div)]
        elif param['strategy'] == 'PPO':
            ppo = ppo[::round((dlen_f - dlen_b) / div)]
            ppo_signal = ppo_signal[::round((dlen_f - dlen_b) / div)]
        elif param['strategy'] == 'Chaikin_AD':
            chaikin_ad = chaikin_ad[::round((dlen_f - dlen_b) / div)]

        try:
            ma = ma[::round((dlen_f - dlen_b) / div)]
            trend = trend[::round((dlen_f - dlen_b) / div)]
            signal_t = signal_t[::round((dlen_f - dlen_b) / div)]
        except:
            pass    
    
    fig, ax = plt.subplots(4, figsize=(15, 10), dpi=120, gridspec_kw={'height_ratios': [9, 2, 2, 2]})
    ax[0].plot(date, price)

    if param['strategy'] == 'RSI':
        pass
    elif param['strategy'] == 'MFI':
        pass
    elif param['strategy'] == 'BBands':
        ax[0].plot(date, bbands_upper, linewidth=1, alpha=0.5, label=f"BB_U_{param['period']}")
        ax[0].plot(date, bbands_middle, linewidth=1, alpha=0.5, label=f"BB_M_{param['period']}")
        ax[0].plot(date, bbands_lower, linewidth=1, alpha=0.5, label=f"BB_L_{param['period']}")
        ax[0].legend()
    elif param['strategy'] == 'Stoch':
        pass
    elif param['strategy'] == 'Stochf':
        pass
    elif param['strategy'] == 'StochRSI':
        pass
    elif param['strategy'] == 'MACD':
        pass
    elif param['strategy'] == 'ROC':
        pass
    elif param['strategy'] == 'ADX':
        pass
    elif param['strategy'] == 'MOM':
        pass
    elif param['strategy'] == 'KAMA':
        pass
    elif param['strategy'] == 'Hilbert':
        pass
    elif param['strategy'] == 'PPO':
        pass
    elif param['strategy'] == 'Chaikin_AD':
        ax[3].plot(date, chaikin_ad, linewidth=1, alpha=0.5, label=f"ChaikinAD_f{param['fastperiod']}_s{param['slowperiod']}")

    try:
        ax[0].plot(date, ma, label=f"MA_{param['period_ma']}")
        ax[0].plot(date, kama, linewidth=1, alpha=0.5, label='KAMA', color='green')
        ax[0].legend()
    except:
        pass

    try:
        ax[1].bar(date, signal_t, label='Signal_T', width=1.0, color='red')
    except:
        ax[1].bar(date, signal, label='Signal', width=1.0, color='red')

    ax[2].bar(date, aposition, label='aPosition')
    ax[3].plot(date, cum_pnl, label='Cum_PnL')

    # ax[1].bar(date, trend, label='Trend')
    # ax[2].plot(date, hilbert_period, label='Hilbert_Period')
    # ax[1].plot(date, hilbert_phase, label='Hilbert_Phase')
    # ax[2].plot(date, hilbert_inphase, label='Hilbert_InPhase')
    # ax[2].plot(date, hilbert_quadrature, label='Hilbert_Quadrature')
    # ax[3].plot(date, hilbert_sine, label='Hilbert_Sine')
    # ax[3].plot(date, hilbert_leadsine, label='Hilbert_Leadsine')
    # ax[3].plot(date, hilbert_integer, label='Hilbert_Integer')

    
    try:
        ax[2].bar(date, cross_tp, label='Cross_TP')
    except:
        try:
            ax[2].bar(date, cross, label='Cross')
        except:
            pass

    ax[0].grid()
    ax[1].grid()
    ax[2].grid()
    ax[3].grid()
    
    ax[1].legend()
    ax[2].legend()
    ax[3].legend()
    # ax[1].set_ylim([-1.1, 1.1])

    if param['trailing_stop']:
        extended_title = ' TS'
    else:
        extended_title = ''
    
    if param['cl_stop'] is True:
        extended_title = extended_title + ' CLs'
    if param['tp_stop'] is True:
        extended_title = extended_title + ' TPs'

    if param['strategy'] == 'RSI':
        plt.suptitle(f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} R{param['rsi_range']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'MFI':
        plt.suptitle(f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} R{param['mfi_range']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'BBands':
        plt.suptitle(f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'Stoch':
        plt.suptitle(f"{param['symbol']} {param['strategy']} fk{param['fastk']} sk{param['slowk']} sd{param['slowd']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'Stochf':
        plt.suptitle(f"{param['symbol']} {param['strategy']} fk{param['fastk']} fd{param['fastd']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'StochRSI':
        plt.suptitle(f"{param['symbol']} {param['strategy']}{param['period']} fk{param['fastk']} fd{param['fastd']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'MACD':
        plt.suptitle(f"{param['symbol']} {param['strategy']} f{param['fastperiod']} s{param['slowperiod']} sig{param['signalperiod']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'ROC':
        plt.suptitle(f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} TH{param['threshold']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'ADX':
        plt.suptitle(f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} RO{param['period_ro']} TH{param['threshold']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'MOM':
        plt.suptitle(f"{param['symbol']} {param['strategy']}{param['period_mom']} R{param['period_range']} MA{param['period_ma']} TH{param['threshold']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'KAMA':
        if param['cross_tp']:
            plt.suptitle(f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} CLr{param['cl_ratio']} Cross_TP De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
        else:
            plt.suptitle(f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'Hilbert':
        # plt.suptitle(f"{param['symbol']} {param['strategy']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
        plt.suptitle(f"{param['symbol']} {param['strategy']} MA{param['period_ma']} CLr{param['cl_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'PPO':
        plt.suptitle(f"{param['symbol']} {param['strategy']} f{param['fastperiod']} s{param['slowperiod']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")
    elif param['strategy'] == 'Chaikin_AD':
        plt.suptitle(f"{param['symbol']} {param['strategy']} f{param['fastperiod']} s{param['slowperiod']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}")

    if down_sampling:
        date = date[::round(len(date) / 30)]
    else:
        date = date[::round((dlen_f - dlen_b) / 30)]

    ax[0].set_xticks(date)
    ax[0].set_xticklabels(date)
    ax[1].set_xticks(date)
    ax[1].set_xticklabels(date)
    ax[2].set_xticks(date)
    ax[2].set_xticklabels(date)
    ax[3].set_xticks(date)
    ax[3].set_xticklabels(date)
    fig.autofmt_xdate()
    f_cum_pnl = float('{:.3f}'.format(cum_pnl[-1]))
    ax[3].annotate(f_cum_pnl, (date[-1], f_cum_pnl), textcoords='offset points', xytext=(0,-12), ha='center')
    
    plt.tight_layout()
    plt.show()

    if param['strategy'] == 'RSI':
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} R{param['rsi_range']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'MFI':
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} R{param['mfi_range']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'BBands':
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'Stoch':
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']} fk{param['fastk']} sk{param['slowk']} sd{param['slowd']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'Stochf':
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']} fk{param['fastk']} fd{param['fastd']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'StochRSI':
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']}{param['period']} fk{param['fastk']} fd{param['fastd']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'MACD':
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']} f{param['fastperiod']} s{param['slowperiod']} sig{param['signalperiod']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'ROC':
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} TH{param['threshold']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'ADX':
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} RO{param['period_ro']} TH{param['threshold']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'MOM':
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']}{param['period_mom']} R{param['period_range']} MA{param['period_ma']} TH{param['threshold']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'KAMA':
        try:
            fig.savefig(data_dir + f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
        except:
            fig.savefig(data_dir + f"{param['symbol']} {param['strategy']}{param['period']} MA{param['period_ma']} CLr{param['cl_ratio']} CrossTP De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'Hilbert':
        # fig.savefig(data_dir + f"{param['symbol']} {param['strategy']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']} MA{param['period_ma']} CLr{param['cl_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'PPO':
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']} f{param['fastperiod']} s{param['slowperiod']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
    elif param['strategy'] == 'Chaikin_AD':
        fig.savefig(data_dir + f"{param['symbol']} {param['strategy']} f{param['fastperiod']} s{param['slowperiod']} CLr{param['cl_ratio']} TPr{param['tp_ratio']} De{param['decay']} Size{param['trading_size']}{extended_title} {param['timeframe']}.png")
