import * as React from 'react';
import {ListButtons} from '../ManageButtons';
import {DataDownload} from '../DataDownload';
import {Box, Checkbox, FormControl, FormControlLabel, FormGroup, Radio, RadioGroup, TextField} from '@material-ui/core';
import {fetchPost, selectUnselectCheckbox} from '../../utils';
import {DataPreparation} from '../DataPreparation/DataPreparation.jsx';

export const REGRESSION_MODELS = {
    MultipleRegression: 1,
};

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

const ROC_METRICS = [
    "Оптимальный порог отсечения",
    "Полнота",
    "Точность",
    "Доля верных ответов",
    "F-мера",
    "Доверительный интервал",
    "Специфичность"
]

const ROC_GRAPHICS_AND_TABLES = [
    "Таблица со значениями каждой точки, по которым строились кривые",
    "Таблица со значениями AUC и остальными метриками, выбранными ранее",
    "График пересечения чувствительности и специфичности",
    "Таблица с точками построения графика пересечения чувствительности и специфичности",
    "Сравнение классификаторов"
]

const TREE_GRAPHICS_AND_TABLES = [
    "Графическое представление дерева",
    "Классификационная таблица, в которой наблюдаемые показатели противопоставляются предсказанным",
    "Показатели построенного дерева",
    "График распределения классов",
    "Блок по предсказанию"
]

let tablesAndGraphOptDict = {}
let rocMetricsDict = {}
let rocGraphicsAndTablesDict = {}
let treeGraphicsAndTablesDict = {}

for (let key in TABLES_AND_GRAPHICS_OPTIONS) {
    tablesAndGraphOptDict[key] = true;
}
for (let key in ROC_METRICS) {
    rocMetricsDict[key] = true;
}
for (let key in ROC_GRAPHICS_AND_TABLES) {
    rocGraphicsAndTablesDict[key] = true;
}
for (let key in TREE_GRAPHICS_AND_TABLES) {
    treeGraphicsAndTablesDict[key] = true;
}

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
        nextText: "Продолжить"
    };

    settings = {
        filePath: '',
        dependent_val_lin_reg: 0,
        dataPrepOption: 0,
        regression_model: 0,
        table_and_graph_options: tablesAndGraphOptDict,
        roc_metrics: rocMetricsDict,
        roc_graphics_and_tables: rocGraphicsAndTablesDict,
        tree_graphics_and_tables: treeGraphicsAndTablesDict,
    };

    paginate = (goNext) => {
        const {currentPage, maxPage} = this.state;
        if (goNext) {
            console.log(this.settings)

            if (currentPage < maxPage) {
                if (this.settings.regression_model == 0) {
                    this.state.maxPage = 4
                } else if
                (this.settings.regression_model == 1) {
                    this.state.maxPage = 4
                }
                else if
                (this.settings.regression_model == 2) {
                    this.state.maxPage = 5
                }
                else if
                (this.settings.regression_model == 3) {
                    this.state.maxPage = 5
                }
                else {
                    this.state.maxPage = 4
                }
                this.setState({currentPage: currentPage + 1});
            } else {
                const {dataPrepOptionId, file} = this.state;

                this.settings.dataPrepOption = dataPrepOptionId;
                this.settings.data = file.path;
                this.settings.dependent_val_lin_reg = 0;

                for (let key in TABLES_AND_GRAPHICS_OPTIONS) {
                    tablesAndGraphOptDict[key] = true;
                }
                for (let key in ROC_METRICS) {
                    rocMetricsDict[key] = true;
                }
                for (let key in ROC_GRAPHICS_AND_TABLES) {
                    rocGraphicsAndTablesDict[key] = true;
                }
                for (let key in TREE_GRAPHICS_AND_TABLES) {
                    treeGraphicsAndTablesDict[key] = true;
                }

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

    selectDependentValLinReg = (id) => {
        this.settings.dependent_val_lin_reg = id;
    }

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
                    title="Для начала основного этапа выберите одну из регрессивных моделей"
                >
                    <FormControl component="fieldset">
                        <RadioGroup
                            name="radio-buttons-group"
                            defaultValue={REGRESSION_MODELS_OPTIONS[this.settings.regression_model]}
                        >
                            {REGRESSION_MODELS_OPTIONS.map((item, idx) => (
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
                return (
                    <Page title="Выберите зависимую переменную из списка">
                        <div>Выберите опции предварительной обработки данных</div>
                        <DataPreparation onClick={this.selectDependentValLinReg}
                                         options={DEPENDENT_PARAMS_OPTIONS}
                                         labelName={"Выбор переменной"}
                                         defaultValue={parseInt(this.settings.dependent_val_lin_reg)}
                        />
                    </Page>
                );
            case 4:
                if (this.settings.regression_model == 0) {
                    return (
                        <Page
                            title="Выберите нужные таблицы и графики"
                        >
                            <FormGroup>
                                {TABLES_AND_GRAPHICS_OPTIONS.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        control={
                                            <Checkbox
                                                defaultChecked={this.settings.table_and_graph_options[idx]}
                                                onClick={() => {
                                                    selectUnselectCheckbox(this, idx, 'table_and_graph_options');
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
                                {TABLES_AND_GRAPHICS_OPTIONS.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        control={
                                            <Checkbox
                                                defaultChecked={this.settings.table_and_graph_options[idx]}
                                                onClick={() => {
                                                    selectUnselectCheckbox(this, idx, 'table_and_graph_options');
                                                }}
                                            />
                                        }
                                        label={item}
                                    />
                                ))}
                            </FormGroup>
                        </Page>
                    );
                } else if (this.settings.regression_model == 2) {
                    return (
                        <Page
                            title="Укажите значения параметров"
                        >
                            <Box
                              component="form"
                              sx={{
                                '& .MuiTextField-root': { m: 1, width: '25ch' },
                              }}
                              noValidate
                              autoComplete="off"
                            >
                                <div>
                                   <TextField
                                       helperText="Максимальная глубина дерева"
                                       variant="outlined"
                                       size="small"
                                       defaultValue="1000"
                                   />
                                    <TextField
                                           helperText="Минимальное количество выборок"
                                           variant="outlined"
                                           size="small"
                                           defaultValue="5"
                                    />
                                </div>
                                <div>
                                    <TextField
                                           helperText="Число признаков для поиска лучшей точки разбиениия"
                                           variant="outlined"
                                           size="small"
                                           defaultValue="5"
                                    />
                                </div>

                                <FormGroup>
                                    <FormControlLabel
                                        control={
                                            <Checkbox defaultChecked />
                                        }
                                        label="Предварительная сортировка"
                                    />
                                </FormGroup>
                            </Box>
                        </Page>
                    );
                } else if (this.settings.regression_model == 4) {
                    return (
                        <Page
                            title="Выберите нужные таблицы и графики"
                        >
                            <FormGroup>
                                {TABLES_AND_GRAPHICS_OPTIONS.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        control={
                                            <Checkbox
                                                defaultChecked={this.settings.table_and_graph_options[idx]}
                                                onClick={() => {
                                                    selectUnselectCheckbox(this, idx, 'table_and_graph_options');
                                                }}
                                            />
                                        }
                                        label={item}
                                    />
                                ))}
                            </FormGroup>
                        </Page>
                    );
                } else if (this.settings.regression_model == 3) {
                    return (
                        <Page
                            title="Выберите нужные таблицы и графики"
                        >
                            <FormGroup>
                                {ROC_METRICS.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        control={
                                            <Checkbox
                                                defaultChecked={this.settings.roc_metrics[idx]}
                                                onClick={() => {
                                                    selectUnselectCheckbox(this, idx, 'roc_metrics');
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
            case 5:
                if (this.settings.regression_model == 2) {
                    return (
                        <Page
                            title="Выберите нужные таблицы и графики"
                        >
                            <FormGroup>
                                {TREE_GRAPHICS_AND_TABLES.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        control={
                                            <Checkbox
                                                defaultChecked={this.settings.tree_graphics_and_tables[idx]}
                                                onClick={() => {
                                                    selectUnselectCheckbox(this, idx, 'tree_graphics_and_tables');
                                                }}
                                            />
                                        }
                                        label={item}
                                    />
                                ))}
                            </FormGroup>
                        </Page>
                    );
                } else if (this.settings.regression_model == 3) {
                    return (
                        <Page
                            title="Выберите нужные таблицы и графики"
                        >
                            <FormGroup>
                                {ROC_GRAPHICS_AND_TABLES.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        control={
                                            <Checkbox
                                                defaultChecked={this.settings.roc_graphics_and_tables[idx]}
                                                onClick={() => {
                                                    selectUnselectCheckbox(this, idx, 'roc_graphics_and_tables');
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
