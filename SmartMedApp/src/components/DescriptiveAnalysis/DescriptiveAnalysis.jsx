import * as React from 'react';

import * as s from './DescriptiveAnalysis.scss';

import {DataDownload} from '../DataDownload';
import {ListButtons} from '../ManageButtons';
import {DataPreparation} from '../DataPreparation/DataPreparation.jsx';
import {Checkbox, FormControlLabel, FormGroup} from '@material-ui/core';
import {fetchPost, selectUnselectCheckbox} from '../../utils';

const DATA_PREP_OPTIONS = ['Средним/модой (численные/категориальные значения)',
    'Введенным значением (требуется ввод для каждого столбца отдельно)',
    'Удаление строк с пропущенными значениями',
    'Медианной/модой (численные/категориальные значения)'
];

const METRICS = [
    'Объем выборки',
    'Среднее по столбцу',
    'Стандартное отклонение по столбцу',
    'Максимальное значение в столбце',
    'Минимальное значение в столбце',
    'Квантили 25, 50, 75',
];

const GRAPH_TYPE = [
    'Матрица корреляций (в виде диаграммы рассеяния)',
    'Гистограмма / столбцовая диаграмма',
    'Матрица корреляций (в численном виде)',
    'Тепловая карта',
    'Точечная диаграмма ',
    'График линейной зависимости',
    'График ящик с усами (диаграмма размаха)',
    'Круговая диаграмма',
    'График логарифмической зависимости',
    'Множественная гистограмма',
];

const Page = (props) => (
    <div>
        <h2>{props.title}</h2>
        <div>{props?.description || ''}</div>
        {props.children}
    </div>
);

let metricsDict = {};
let graphicsDict = {};

for (let key in METRICS) {
    metricsDict[key] = true;
}

for (let key in GRAPH_TYPE) {
    graphicsDict[key] = true;
}

export class DescriptiveAnalysis extends React.Component {
    state = {
        currentPage: 0,
        maxPage: 3,
        nextText: "Продолжить"
    };

    settings = {
        filePath: '',
        dataPrepOption: 0,
        metrics: metricsDict,
        graphics: graphicsDict,
    };

    paginate = (goNext) => {
        const {currentPage, maxPage} = this.state;
        console.log(this.settings.dataPrepOption)
        console.log(this.settings.metrics)
        console.log(this.settings.graphics)
        if (goNext) {
            if (currentPage < maxPage) {
                this.setState({currentPage: currentPage + 1});
            } else {
                void fetchPost('descriptive', this.settings);
                this.setState({currentPage: 1});

                for (let key in METRICS) {
                    metricsDict[key] = true;
                }
                for (let key in GRAPH_TYPE) {
                    graphicsDict[key] = true;
                }

                this.settings = {
                    filePath: '',
                    dataPrepOption: 0,
                };
                this.props.onExit();
            }
        } else {
            if (currentPage > 0) {
                this.setState({currentPage: currentPage - 1});
            } else {
                this.props.onExit();
            }
        }
    };

    getNextText = () => {
        if (this.state.currentPage < this.state.maxPage) {
            return "Продолжить";
        } else {
            return "Завершить";
        }
    };

    selectDataPrepType = (id) => {
        this.settings.dataPrepOption = id;
    };

    onDataLoad = (event) => {
        if (event.target.files && event.target.files[0]) {
            this.settings.filePath = event.target.files[0].path;
        }
    };

    openCurrentPage = () => {
        const {currentPage} = this.state;
        switch (currentPage) {
            case 0:
                return (<Page
                    title="Загрузите данные"
                >
                    <DataDownload onLoad={this.onDataLoad}/>
                </Page>);
            case 1:
                return (<Page
                    title="Предварительная обработка данных"
                >
                    <div className={s.selectDataPrepType__text}>
                        Выберите опции предварительной обработки данных
                    </div>
                    <DataPreparation onClick={this.selectDataPrepType}
                                     options={DATA_PREP_OPTIONS}
                                     labelName={"Выбор опции"}
                                     defaultValue={parseInt(this.settings.dataPrepOption)}
                    />
                </Page>);
            case 2:
                return (
                    <Page
                        title="Выбор статистических метрик"
                    >
                        <FormGroup className={s.choseStatisticMetrics__items}>
                            {METRICS.map((item, idx) => (
                                <FormControlLabel
                                    className={s.choseStatisticMetrics__item}
                                    key={`m-${item}`}
                                    control={
                                        <Checkbox
                                            defaultChecked={this.settings.metrics[idx]}
                                            onClick={() => {
                                                selectUnselectCheckbox(this, idx, 'metrics');
                                            }}
                                        />
                                    }
                                    label={item}
                                />
                            ))}
                        </FormGroup>
                    </Page>
                );
            case 3:
                return (
                    <Page
                        title="Выбор графиков для реализации"
                    >
                        <FormGroup className={s.descriptiveAnalysis__items}>
                            {GRAPH_TYPE.map((item, idx) => (
                                <FormControlLabel
                                    className={s.descriptiveAnalysis__item}
                                    key={`g-${item}`}
                                    label={item}
                                    control={
                                        <Checkbox
                                            defaultChecked={this.settings.graphics[idx]}
                                            onClick={() => {
                                                selectUnselectCheckbox(this, idx, 'graphics');
                                            }}
                                        />
                                    }
                                />
                            ))}
                        </FormGroup>
                    </Page>
                );
            default:
                console.error(`unknown page: ${currentPage}`);
        }
    };

    render() {
        return (
            <div className="ListButtons">
                {this.openCurrentPage()}
                <ListButtons onClick={this.paginate} nextText={this.getNextText}/>
            </div>
        );
    }

}
