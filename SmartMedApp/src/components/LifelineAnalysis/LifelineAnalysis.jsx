import * as React from 'react';
import {ListButtons} from '../ManageButtons';
import {DataDownload} from '../DataDownload';
import {Box, Checkbox, FormControl, FormControlLabel, FormGroup, Radio, RadioGroup, TextField} from '@material-ui/core';
import {fetchGet, fetchPost, selectUnselectCheckbox} from '../../utils';
import {DataPreparation} from '../DataPreparation/DataPreparation.jsx';

export const REGRESSION_MODELS = {
    MultipleRegression: 1,
};

const DATA_PREP_OPTIONS = ['Средним/модой (численные/категориальные значения)',
    'Удаление строк с пропущенными значениями',
    'Медианной/модой (численные/категориальные значения)'
];

const MODELS_OPTIONS = [
    "Сравнение выживаемости в двух выборках",
    "Анализ выживаемости в одной выборке"

];

let DEPENDENT_PARAMS_OPTIONS = [
    "",
];

const METHODS_OPTIONS = [
    "Таблица времен жизни",
    "Кривая выживаемости",
    "Медиана выживаемости"
];

const CRITERIA_METRICS = [
    "Логранговый критерий",
    "Критерий Гехана",
    "Таблицы времен жизни",
    "Кривые выживаемости",
    "Медианы выживаемости"
]




let criteriaDict = {}
let methodsDict = {}

for (let key in METHODS_OPTIONS) {
    methodsDict[key] = true;
}
for (let key in CRITERIA_METRICS) {
    criteriaDict[key] = true;
}


const Page = (props) => (
    <div>
        <h2>{props.title}</h2>
        <div>{props?.description || ''}</div>
        {props.children}
    </div>
);

export class LifelineAnalysis extends React.Component {

    state = {
        currentPage: 0,
        maxPage: 4,
        nextText: "Продолжить"
    };

    settings = {
        filePath: '',
        dependent_val: DEPENDENT_PARAMS_OPTIONS[0],
        dataPrepOption: 0,
        regression_model: 0,
        methods: methodsDict,
        criteria: criteriaDict,
    };

    paginate = (goNext) => {
        const {currentPage, maxPage} = this.state;
        if (goNext) {
            console.log(this.settings)

            if (currentPage < maxPage) {
                this.setState({currentPage: currentPage + 1});

                if (this.settings.regression_model == 0) {
                    this.state.maxPage = 3
                } else if
                (this.settings.regression_model == 1) {
                    this.state.maxPage = 3
                }

            } else {
                void fetchPost('lifeline', this.settings);

                this.settings.dataPrepOption = 0;
                this.settings.filePath = '';
                this.settings.regression_model = 0;
                this.settings.dependent_val = DEPENDENT_PARAMS_OPTIONS[0];

                for (let key in METHODS_OPTIONS) {
                     methodsDict[key] = true;
                    }
                for (let key in CRITERIA_METRICS) {
                        criteriaDict[key] = true;
                    }

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

    selectRadio = (id, field) => {
        this.settings[field] = id;
    };

    selectDataPrepType = (id) => {
        this.settings.dataPrepOption = id;
    };


    onDataLoad = (event) => {
        if (event.target.files && event.target.files[0]) {
            this.settings.filePath = event.target.files[0].path;
        }

        const API = 'http://127.0.0.1:15001/api';
        const result = fetch(API + '/lifeline/get_class_columns', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=utf-8',
            },
            body: JSON.stringify(this.settings)
        })
        result
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                DEPENDENT_PARAMS_OPTIONS = Object.values(data)
            })
            .catch((error) => {
                console.log('error', error);
            })
    };

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
                    <DataPreparation onClick={this.selectDataPrepType}
                                     options={DATA_PREP_OPTIONS}
                                     labelName={"Выбор опции"}
                                     defaultValue={parseInt(this.settings.dataPrepOption)}
                    />
                </Page>);
            case 2:
                return (<Page
                    title="Для начала основного этапа выберите одну из опций"
                >
                    <FormControl component="fieldset">
                        <RadioGroup
                            name="radio-buttons-group"
                            defaultValue={MODELS_OPTIONS[this.settings.regression_model]}
                        >
                            {MODELS_OPTIONS.map((item, idx) => (
                                <FormControlLabel
                                    key={`m-${item}`}
                                    control={
                                        <Radio
                                            onClick={() => {
                                                this.selectRadio(idx, 'regression_model');
                                            }}
                                        />
                                    }
                                    label={item}
                                    value={item}
                                />
                            ))}
                        </RadioGroup>
                    </FormControl>
                </Page>);
            case 3:
                if (this.settings.regression_model == 0) {
                    return (
                        <Page
                            title="Выберите нужные таблицы и графики"
                        >
                            <FormGroup>
                                {CRITERIA_METRICS.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        control={
                                            <Checkbox
                                                defaultChecked={this.settings.criteria[idx]}
                                                onClick={() => {
                                                    selectUnselectCheckbox(this, idx, 'criteria');
                                                }}
                                            />
                                        }
                                        label={item}
                                    />
                                ))}
                            </FormGroup>
                        </Page>
                    );
                } else if (this.settings.regression_model == 1) {
                    return (
                        <Page
                            title="Выберите нужные таблицы и графики"
                        >
                            <FormGroup>
                                {METHODS_OPTIONS.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        control={
                                            <Checkbox
                                                defaultChecked={this.settings.methods[idx]}
                                                onClick={() => {
                                                    selectUnselectCheckbox(this, idx, 'methods');
                                                }}
                                            />
                                        }
                                        label={item}
                                    />
                                ))}
                            </FormGroup>
                        </Page>
                    );
                }
            default:
                console.error(`unknown page: ${currentPage}`);
        }
    };

    render() {
        return (
            <div>
                {this.openCurrentPage()}
                <ListButtons onClick={this.paginate} nextText={this.getNextText}/>
            </div>
        );
    }

}
