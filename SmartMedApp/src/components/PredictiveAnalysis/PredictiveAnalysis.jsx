import * as React from 'react';
import {ListButtons} from '../ManageButtons';
import {DataDownload} from '../DataDownload';
import {Checkbox, FormControl, FormControlLabel, FormGroup, Radio, RadioGroup} from '@material-ui/core';
import {fetchPost} from '../../utils';
import {DataPreparation} from '../DataPreparation/DataPreparation.jsx';

const DATA_PREP_OPTIONS = ['Средним/модой (численные/категориальные значения)',
    'Введенным значением (требуется ввод для каждого столбца отдельно)',
    'Удаление строк с пропущенными значениями',
    'Медианной/модой (численные/категориальные значения)'
];

const REGRESSION_MODELS_OPTIONS = [
    "Множественная (линейная) регрессия",
    "Логистическая регрессия",
    "Деревья классификации",
    "ROC-анализ",
    "Полиномиальная регрессия",
];

const DEPENDENT_PARAMS_OPTIONS = [
    "ПЗ: до лечения",
    "ПЗ: 6 месяцев после лечения",
    "ВГД: до лечения",
    "ВГД: 6 месяцев после лечения",
    "Тип операции",
];

const TABLES_AND_GRAPHICS_OPTIONS = [
    "Таблица с критериями качества построенной модели",
    "Таблица с критериями значимости для каждой независимой переменной",
    "Полученное уравнение регрессии с возможностью ввода собственных переменных",
    "Таблица с анализами остатков",
    "Графики распределения остатков",
];

const Page = (props) => (
    <div>
        <h2>{props.title}</h2>
        <div>{props?.description || ''}</div>
        {props.children}
    </div>
);

export class PredictiveAnalysis extends React.Component {

    state = {
        currentPage: 0,
        maxPage: 4,
        dataPrepOptionId: -1,
        fileOne: null,
        fileTwo: null,
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
                void fetchPost('api/predictive', this.settings);
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

    selectUnselect = (item, field = '') => {
        const index = this.settings[field].indexOf(item);
        if (index !== -1) {
            this.settings[field].splice(index, 1);
        } else {
            this.settings[field].push(item);
        }
    };

    openCurrentPage = (props) => {
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
                    <div>Выберите опции предварительной обработки данных</div>
                    <DataPreparation onClick={this.selectDataPrepType} options={DATA_PREP_OPTIONS}/>
                </Page>);
            case 2:
                return (<Page
                    title="Для начала основного этапа выберите одну из регрессивных моделей"
                >
                    <FormControl component="fieldset">
                        <RadioGroup name="radio-buttons-group">
                            {REGRESSION_MODELS_OPTIONS.map((item, idx) => (
                                <FormControlLabel
                                    key={`m-${item}`}
                                    control={<Radio onClick={() => {
                                        this.selectUnselect(idx, 'metrics');
                                    }}/>}
                                    label={item}
                                    value={item}
                                />
                            ))}
                        </RadioGroup>
                    </FormControl>
                </Page>);
            case 3:
                return (<Page
                    title="Выберите зависимую переменную из списка"
                >
                    <DataPreparation onClick={this.selectDataPrepType} options={DEPENDENT_PARAMS_OPTIONS}/>
                </Page>);
            case 4:
                return (
                    <Page
                        title="Выберите нужные таблицы"
                    >
                        <FormGroup>
                            {TABLES_AND_GRAPHICS_OPTIONS.map((item, idx) => (
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
