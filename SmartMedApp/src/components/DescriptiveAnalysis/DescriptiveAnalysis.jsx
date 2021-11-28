import * as React from 'react';

import * as s from './DescriptiveAnalysis.scss';

import {DataDownload} from '../DataDownload';
import {ListButtons} from '../ManageButtons';
import {DataPreparation} from './DataPreparation.jsx';
import {Checkbox, FormControlLabel, FormGroup} from '@material-ui/core';
import {fetchPost} from '../../utils';

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

const Page = (props) => (
    <div>
        <h2>{props.title}</h2>
        <div>{props?.description || ''}</div>
        {props.children}
    </div>
);

const GRAPH_TYPE = [
    'Матрица корреляций (в виде диаграммы рассеяния)',
    'Гистограмма / столбцовая диаграмма',
    'Матрица корреляций (в численном виде)',
    'Тепловая карта',
    'Точечная диаграмма ',
    'График линейной зависимости',
    'График ящик с усами (диаграмма размаха)',
    'Столбцовая диаграмма',
    'Круговая диаграмма',
    'График логарифмической зависимости',
    'Множественная гистограмма',
];

export class DescriptiveAnalysis extends React.Component {

    state = {
        currentPage: 0,
        maxPage: 3,
        dataPrepOptionId: -1,
        file: null,
    };

    settings = {
        data: '',
        dataPrepOption: 0,
        metrics: [],
        graphics: [],
    };

    paginate = (goNext) => {
        const {currentPage, maxPage} = this.state;
        if (goNext) {
            if (currentPage < maxPage) {
                this.setState({currentPage: currentPage + 1});
            } else {
                const {dataPrepOptionId, file} = this.state;
                this.settings.dataPrepOption = dataPrepOptionId;
                console.log(file);
                this.settings.data = file.path;
                void fetchPost('api/descriptive', this.settings);
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

    selectDataPrepType = (id) => this.setState({dataPrepOptionId: id});

    onDataLoad = (event) => {
        if (event.target.files && event.target.files[0]) {
            this.setState({file: event.target.files[0]});
            this.readDataFromFile(event.target.files[0]);
        }
    };

    readDataFromFile = (path) => {
        // const FR = new FileReader();
        // console.log(path);
        // FR.addEventListener('load', (event) => {
        //     this.settings.data = event.target.result;
        // });
        // FR.readAsText(path, 'UTF-8');
    };

    selectUnselect = (item, field = '') => {
        const index = this.settings[field].indexOf(item);
        if (index !== -1) {
            this.settings[field].splice(index, 1);
        } else {
            this.settings[field].push(item);
        }
    };

    openCurrentPage = () => {
        const {currentPage} = this.state;
        switch (currentPage) {
            case 0:
                return <DataDownload onLoad={this.onDataLoad}/>;
            case 1:
                return <DataPreparation onClick={this.selectDataPrepType} options={DATA_PREP_OPTIONS}/>;
            case 2:
                return (
                    <Page
                        title="Метрики"
                        description="Выбор статистических метрик"
                    >
                        <FormGroup>
                            {METRICS.map((item, idx) => (
                                <FormControlLabel
                                    key={`m-${item}`}
                                    control={<Checkbox onClick={() => {
                                        this.selectUnselect(idx, 'metrics');
                                    }}/>}
                                    label={item}
                                />
                            ))}
                        </FormGroup>
                    </Page>
                );
            case 3:
                return (
                    <Page
                        title="Визуализация"
                        description="Выбор графиков для реализации"
                    >
                        <FormGroup className={s.descriptiveAnalysis}>
                            {GRAPH_TYPE.map((item, idx) => (
                                <FormControlLabel
                                    key={`g-${item}`}
                                    control={<Checkbox onClick={() => {
                                        this.selectUnselect(idx, 'graphics');
                                    }}/>}
                                    label={item}
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
            <div>
                {this.openCurrentPage()}
                <ListButtons onClick={this.paginate}/>
            </div>
        );
    }

}
