import * as React from 'react';
import {ListButtons} from '../ManageButtons';
import {DataDownload} from '../DataDownload';
import {Checkbox, FormControl, FormControlLabel,
    FormGroup, Radio, RadioGroup} from '@material-ui/core';
import {fetchPost, selectUnselectCheckbox} from '../../utils';
import {DataPreparation} from '../DataPreparation/DataPreparation.jsx';


const DATA_PREP_OPTIONS = ['Средним/модой (численные/категориальные значения)',
    'Удаление строк с пропущенными значениями',
    'Медианной/модой (численные/категориальные значения)'
];

const VARIABLE_TYPES = [
    "Непрерывные",
    "Категориальные"
]

const CONTINUOUS_VARS_METHODS = [
    'Тест Колмогорова-Смирнова',
    'T-критерий Стьюдента для зависимых переменных',
    'T-критерий Стьюдента для независимых переменных',
    'U-критерий Манна-Уитни',
    'T-критерий Уилкоксона',
];

const CATEGORIAL_VARS_METHODS = [
    'Хи квадрат Пирсона',
    'Чувствительность и специфичность',
    'Подсчёт отношения шансов',
    'Подсчёт отношения рисков'
];

const Page = (props) => (
    <div>
        <h2>{props.title}</h2>
        <div style={{marginBottom: 20}}>{props?.description || ''}</div>
        {props.children}
    </div>
);

let ContinuousMethodsDict = {};
let CategorialMethodsDict = {};

for (let key in CONTINUOUS_VARS_METHODS) {
    ContinuousMethodsDict[key] = true;
}

for (let key in CATEGORIAL_VARS_METHODS) {
    CategorialMethodsDict[key] = true;
}

export class ComparativeAnalysis extends React.Component {

    state = {
        currentPage: 0,
        maxPage: 3,
    };

    settings = {
        filePath: '',
        dataPrepOption: 0,
        var_type: 0,
        continuous_methods: ContinuousMethodsDict,
        categorial_methods: CategorialMethodsDict
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

    paginate = (goNext) => {
        console.log(this.settings)
        console.log(this.state)
        const {currentPage, maxPage} = this.state;
        if (goNext) {
            if (currentPage < maxPage) {
                this.setState({currentPage: currentPage + 1});
            } else {
                console.log(this.settings)
                void fetchPost('comparative', this.settings);

                this.setState({
                    currentPage: 1,
                });

                this.settings.dataPrepOption = 0
                this.settings.var_type = 0
                this.settings.filePath = ""

                for (let key in CONTINUOUS_VARS_METHODS) {
                    ContinuousMethodsDict[key] = true;
                }

                for (let key in CATEGORIAL_VARS_METHODS) {
                    CategorialMethodsDict[key] = true;
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


    selectRadio = (id, field) => {
        this.settings[field] = id;
    };

    onDataLoad = (event) => {
        if (event.target.files && event.target.files[0]) {
            this.settings.filePath = event.target.files[0].path;
        }
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
                    description="Выберите опции предварительной обработки данных"
                >
                    <DataPreparation onClick={this.selectDataPrepType}
                                     options={DATA_PREP_OPTIONS}
                                     labelName={"Выбор опции"}
                                     defaultValue={parseInt(this.settings.dataPrepOption)}
                    />
                </Page>);
            case 2:
                return(
                    <Page
                        title="Выбор типа переменных"
                        description="Выберите тип переменных"
                    >
                        <FormControl component="fieldset">
                            <RadioGroup
                                name="radio-buttons-group"
                                defaultValue={VARIABLE_TYPES[this.settings.var_type]}
                            >
                                {VARIABLE_TYPES.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        control={
                                            <Radio
                                                onClick={() => {
                                                    this.selectRadio(idx, 'var_type');
                                                }}
                                            />
                                        }
                                        label={item}
                                        value={item}
                                    />
                                ))}
                            </RadioGroup>
                        </FormControl>
                    </Page>
                );
            case 3:
                if (this.settings.var_type == 0) {
                    return (
                        <Page
                            title="Выберите метод сравнения"
                        >
                            <FormGroup>
                                {CONTINUOUS_VARS_METHODS.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        label={item}
                                        control={
                                            <Checkbox
                                                defaultChecked={this.settings.continuous_methods[idx]}
                                                onClick={() => {
                                                    selectUnselectCheckbox(this, idx, 'continuous_methods');
                                                }}
                                            />
                                        }
                                    />
                                ))}
                            </FormGroup>
                        </Page>
                    );
                }
                else {
                    return (
                        <Page
                            title="Выберите метод сравнения"
                        >
                            <FormGroup>
                                {CATEGORIAL_VARS_METHODS.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        label={item}
                                        control={
                                            <Checkbox
                                                defaultChecked={this.settings.categorial_methods[idx]}
                                                onClick={() => {
                                                    selectUnselectCheckbox(this, idx, 'categorial_methods');
                                                }}
                                            />
                                        }
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
