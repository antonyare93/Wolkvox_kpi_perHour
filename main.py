import datetime
import sendTelegram
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import wolkvox_api as wv

while True:
    f_val = datetime.datetime.now().strftime("%M%S")
    if datetime.datetime.now().strftime("%H") in ['09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19']:
        if f_val == '0101' or datetime.datetime.now().strftime("%H%M%S") == '192000':
            fechaActual1 = str(int(datetime.datetime.now().strftime("%Y%m%d%H")) - 1)
            if datetime.datetime.now().strftime("%H%M") == '1920':
                fechaActual1 = datetime.datetime.now().strftime("%Y%m%d%H")
            j_resultado = wv.skill4(fechaActual1)
            j_workforce = wv.skill5(fechaActual1)
            j_conexion = wv.agent6(fechaActual1)

            if j_resultado['code'] == '200':
                tablaTrafico = pd.DataFrame(j_resultado['data'])
                tablaWorkforce = pd.DataFrame(j_workforce['data'])
                tablaConexion = pd.DataFrame(j_conexion['data'])

                tablaConexion = tablaConexion[tablaConexion.login_time != '00:00:00']

                tablaConexion.pop('calls')
                tablaConexion.pop('inbound')
                tablaConexion.pop('outbound')
                tablaConexion.pop('internal')
                tablaConexion.pop('ready_time')
                tablaConexion.pop('inbound_time')
                tablaConexion.pop('outbound_time')
                tablaConexion.pop('acw_time')
                tablaConexion.pop('ring_time')
                tablaConexion.pop('aht')
                tablaConexion.pop('occupancy')

                tablaWorkforce.pop('aht')
                tablaWorkforce.pop('inbound_calls')

                tablaTrafico.pop('skill_id')
                tablaTrafico.pop('abandon')
                tablaTrafico.pop('aht')
                tablaTrafico.pop('asa')
                tablaTrafico.pop('ata')
                tablaTrafico.pop('service_level_10seg')
                tablaTrafico.pop('service_level_30seg')

                tablaWorkforce = tablaWorkforce.rename(columns={'hour': 'Hora',
                                                                'inbound_calls_unique_customers': 'Unicos por hora',
                                                                'agents_needed': 'Agentes requeridos'})

                tablaTrafico = tablaTrafico.rename(columns={'hour': 'Hora', 'inbound_calls': 'Entrantes',
                                                            'answer_calls': 'Atendidas', 'abandon_calls': 'Abandonadas',
                                                            'service_level_20seg': 'Nv. Servicio (%)'})
                tablaTrafico['Nv. Servicio (%)'] = tablaTrafico['Nv. Servicio (%)'].str.strip(' %')
                tablaConexion['hour'] = tablaConexion['hour'].str.strip(':00').astype('string')

                tablaConexion = tablaConexion.astype({'login_time': 'datetime64[ns]', 'aux_time': 'datetime64[ns]'})
                tablaConexion['Agentes_conectados'] = tablaConexion['login_time'] - tablaConexion['aux_time']
                tablaConexion['Agentes_conectados'] = tablaConexion['Agentes_conectados'].astype('string')

                tablaConexion.pop('login_time')
                tablaConexion.pop('aux_time')

                tablaConexion['Agentes_conectados'] = tablaConexion['Agentes_conectados'].str.strip('0 days ').\
                    astype('string')
                tablaConexion['Agentes_conectados'] = tablaConexion['Agentes_conectados'].str.slice(stop=2)
                tablaConexion['Agentes_conectados'] = tablaConexion['Agentes_conectados'].str.strip(':'). \
                    astype('string')

                tablaConexion = tablaConexion.astype({'Agentes_conectados': 'int64'})

                tablaWorkforce = tablaWorkforce.astype({'Hora': 'int64', 'Agentes requeridos': 'int64'})

                tablaTrafico = tablaTrafico.astype({'Hora': 'int64', 'Entrantes': 'int64', 'Atendidas': 'int64',
                                                    'Abandonadas': 'int64', 'Nv. Servicio (%)': 'float64'})

                tablaTrafico.set_index('Hora')

                column_label = tablaTrafico.columns.tolist()
                column_label.pop(0)
                row_labels = tablaTrafico['Hora'].tolist()

                index_pos = np.arange(len(row_labels)) + 0.5
                col_width = 0.3

                tablaTrafico['Atendidas en 20'] = tablaTrafico['Entrantes'] * (
                            tablaTrafico['Nv. Servicio (%)'] / 100)

                # tablaTrafico.plot(marker='o')
                plt.style.use('ggplot')
                fig, ax1 = plt.subplots()

                ax1.bar(index_pos, tablaTrafico['Atendidas'].tolist(), col_width, label='Atendidas',
                        color='green')
                ax1.bar(index_pos, tablaTrafico['Abandonadas'].tolist(), col_width, label='Abandonadas',
                        bottom=tablaTrafico['Atendidas'].tolist(), color='red')
                ax1.scatter(index_pos, tablaTrafico['Entrantes'].tolist(), label='Total',
                            color='grey')
                ax1.legend(loc='upper left', bbox_to_anchor=(-0.01, 1.18), ncol=2)

                ax2 = ax1.twinx()

                ax2.plot(index_pos, tablaTrafico['Nv. Servicio (%)'].tolist(), marker='o',
                         color='orange', label='Nv. Servicio (%)')
                ax2.legend(loc='upper right', bbox_to_anchor=(1.01, 1.112))
                fig.tight_layout()

                plt.xticks([])

                tabla_datos = plt.table(cellText=[tablaTrafico['Entrantes'].tolist(), tablaTrafico['Atendidas'].
                                        tolist(), tablaTrafico['Abandonadas'].tolist(),
                                                  tablaTrafico['Nv. Servicio (%)'].tolist()],
                                        rowLabels=column_label, colLabels=row_labels, loc='bottom')
                tabla_datos.set_fontsize(8)
                plt.subplots_adjust(left=0.2, bottom=0.2, top=0.85)
                # plt.show()
                plt.savefig(f'horas/horas_{fechaActual1}.png')
                plt.close()

                total20 = tablaTrafico['Atendidas en 20'].sum()
                totalEntrantes = tablaTrafico['Entrantes'].sum()
                totalAtendidas = tablaTrafico['Atendidas'].sum()
                totalAbandonadas = tablaTrafico['Abandonadas'].sum()

                ns_dia = ((total20 / totalEntrantes) * 100).__round__(2)
                at_dia = ((totalAtendidas / totalEntrantes) * 100).__round__(2)
                ab_dia = ((totalAbandonadas / totalEntrantes) * 100).__round__(2)

                tablaTrafico = tablaTrafico.set_index('Hora').join(tablaWorkforce.set_index('Hora'))
                tablaTrafico = tablaTrafico.join(tablaConexion)

                tablaTrafico.pop('hour')

                tablaTrafico['Presicion dimensionamiento'] = (((tablaTrafico['Agentes_conectados'] -
                                                              tablaTrafico['Agentes requeridos']) / tablaTrafico[
                    'Agentes requeridos'])*100).__round__(2)

                plt.style.use('ggplot')
                fig, ax1 = plt.subplots()

                ax1.bar(index_pos, tablaTrafico['Agentes requeridos'].tolist(), col_width, label='Requeridos',
                        color='green')
                ax1.scatter(index_pos, tablaTrafico['Agentes_conectados'].tolist(), label='Conectados',
                            color='grey')
                ax1.legend(loc='upper left', bbox_to_anchor=(-0.01, 1.18), ncol=1)

                ax2 = ax1.twinx()

                ax2.plot(index_pos, tablaTrafico['Presicion dimensionamiento'].tolist(), marker='o',
                         color='orange', label='Presicion dimensionamiento (%)')
                ax2.legend(loc='upper right', bbox_to_anchor=(1.01, 1.112))
                fig.tight_layout()

                plt.xticks([])

                column_label = ['Requeridos', 'Conectados', 'Presición (%)']

                tabla_datos = plt.table(cellText=[tablaTrafico['Agentes requeridos'].tolist(),
                                                  tablaTrafico['Agentes_conectados'].tolist(),
                                                  tablaTrafico['Presicion dimensionamiento'].tolist()],
                                        rowLabels=column_label, colLabels=row_labels, loc='bottom')
                tabla_datos.set_fontsize(8)
                plt.subplots_adjust(left=0.2, bottom=0.2, top=0.85)
                # plt.show()
                plt.savefig(f'workforce/workforce_{fechaActual1}.png')
                plt.close()

                mensaje = f'Reporte {fechaActual1[:8]} - Corte de las {fechaActual1[8:]}:59\n\nNivel de servicio: {ns_dia}%\nNivel atención: {at_dia}%\nNivel abandono: {ab_dia}%\n\nEntrantes: ' \
                          f'{totalEntrantes}\nAtendidas: {totalAtendidas}\nAbandonadas: {totalAbandonadas}'
                sendTelegram.enviar_telegram(foto={'photo': open(f'horas_{fechaActual1}.png', 'rb')},
                                             mensaje=mensaje)
                mensaje2 = f'Dimensionamiento {fechaActual1[:8]} - Corte de las {fechaActual1[8:]}:59'
                sendTelegram.enviar_telegram(foto={'photo': open(f'workforce_{fechaActual1}.png', 'rb')},
                                             mensaje=mensaje2)
