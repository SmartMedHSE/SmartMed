import * as React from 'react';
import {ListButtons} from '../ManageButtons';
import {Button, Checkbox, FormControl, FormControlLabel, FormGroup, Radio, RadioGroup} from '@material-ui/core';
import {fetchPost, selectUnselectCheckbox} from '../../utils';
import * as cn from "classnames";
import * as ss from "./BioequivalenceAnalysis.scss"

const PLAN_SELECTION = [
    "Перекрёстный дизайн",
    "Параллельный дизайн"
];

const METHOD_OF_VERIFICATION = [
    "Критерий Колмогорова-Смирнова",
    "Критерий Шапиро-Уилка"
];

const HOMOGENEITY_METHODS = [
    "F-критерий",
    "Критерий Левена"
];

const TABLE_SELECTION = [
    "Средние площади под графиком по каждому препарату",
    "Результаты двухфакторного дисперсионного анализа",
    "Данные описательной статистики",
    "Результаты оценки биоэквивалентности"
];

const VISUALIZATION_SELECTION = [
    "Индивидуальные графики для пациентов c концентрациями обоих препаратов",
    "Графики со средними концентрациями препаратов по группам",
    "График, где данные обобщены по двум препаратам"
];

const PARAL_TABLE_SELECTION = [
    "Выполнение критериев",
    "AUC, максимальная концентрация, время достижениия максимальной концентрации",
    "Результаты классического дисперсионного анализа (ANOVA)",
    "Результаты оценки биоэквивалентности",
    "Данные описательной статистики"
];

const PARAL_GRAPHICS = [
    "Прологарифмированный график зависимости концентрации препарата " +
    "от времени для всех пациентов в каждой группе",
    "График зависимости концентрации препарата от времени для всех пациентов в каждой группе",
    "Обобщенный график зависимости концентрации препарата от времени для каждой группы",
    "Прологарифмированный обобщённый график зависимости концентрации препарата " +
    "от времени для каждой группы",
];

const Page = (props) => (
    <div>
        <h2>{props.title}</h2>
        <div>{props?.description || ''}</div>
        {props.children}
    </div>
);

let tableDict = {};
let visualisationDict = {};
let paralTableDict = {};
let paralGraphicsDict = {}

for (let key in TABLE_SELECTION) {
    tableDict[key] = true;
}

for (let key in VISUALIZATION_SELECTION) {
    visualisationDict[key] = true;
}

for (let key in PARAL_TABLE_SELECTION) {
    paralTableDict[key] = true;
}

for (let key in PARAL_GRAPHICS) {
    paralGraphicsDict[key] = true;
}

export class BioequivalenceAnalysis extends React.Component {

    state = {
        currentPage: 0,
        maxPage: 4,
        fileOneName: "",
        fileTwoName: "",
    };

    settings = {
        fileOne: "",
        fileTwo: "",
        plan: 0,
        method: 0,
        homogeneity_method: 0,
        table: tableDict,
        paral_table: paralTableDict,
        visualisation: visualisationDict,
        paral_graphics: paralGraphicsDict
    };

    getNextText = () => {
        if (this.state.currentPage < this.state.maxPage) {
            return "Продолжить";
        } else {
            return "Завершить";
        }
    };

    paginate = (goNext) => {
        console.log(this.settings)
        console.log(this.state)
        const {currentPage, maxPage} = this.state;
        if (goNext) {
            if (currentPage < maxPage) {
                this.setState({currentPage: currentPage + 1});

                if (this.settings.plan == 0) {
                    this.state.maxPage = 4
                } else {
                    this.state.maxPage = 5
                }
            } else {
                console.log(this.settings)
                void fetchPost('bioequivalence', this.settings);

                this.setState({
                    currentPage: 1,
                    fileOneName: "",
                    fileTwoName: "",
                });

                this.settings.plan = 0
                this.settings.method = 0
                this.settings.homogeneity_method = 0
                this.settings.fileOne = ""
                this.settings.fileTwo = ""

                for (let key in TABLE_SELECTION) {
                    tableDict[key] = true;
                }

                for (let key in VISUALIZATION_SELECTION) {
                    visualisationDict[key] = true;
                }

                for (let key in PARAL_TABLE_SELECTION) {
                    paralTableDict[key] = true;
                }

                for (let key in PARAL_GRAPHICS) {
                    paralGraphicsDict[key] = true;
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

    onDataLoad = (event, field) => {
        const file = event.target.files[0]
        if (event.target.files && file) {
            this.settings[field] = file.path;
            this.state[field + "Name"] = file.name;
        }

    };

    selectRadio = (id, field) => {
        this.settings[field] = id;
    };

    openCurrentPage = (props) => {
        const {currentPage} = this.state;
        switch (currentPage) {
            case 0:
                return (
                    <Page
                        title="Укажите, с какой выборкой проводится работа"
                    >
                        <FormControl component="fieldset">
                            <RadioGroup
                                name="radio-buttons-group"
                                defaultValue={PLAN_SELECTION[this.settings.plan]}
                            >
                                {PLAN_SELECTION.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        control={
                                            <Radio
                                                onClick={() => {
                                                    this.selectRadio(idx, 'plan');
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
            case 1:
                if (this.settings.plan == 0) {
                    return (<Page
                        title="Загрузка данных"
                    >
                        Данные должны быть загружены в формате ".хlsx", ".хs" или ".сsv".
                        <br/>
                        <br/>
                        Необходима загрузка двух файлов.
                        <br/>
                        <br/>
                        Первый файл должен содержать информацию о пациентах, принимавших первым тестовый препарат, а за
                        ним
                        - референсный. Второй файл должен содержать информацию о пациентах, которые сначала принимали
                        референсный препарат, затем - тестовый.
                        <br/>
                        <br/>
                        Необходимо, чтобы в первой строке каждого файла был указан момент времени (в часах), в который
                        была
                        зафиксирована концентрация.
                        <br/>
                        <br/>
                        В первом столбце каждого файла нужно указать порядковый номер пациента.
                        <div className={cn(ss.dataDownload__download_btns_and_texts)}>
                            <div className={cn(ss.dataDownload__download_btns)}>
                                <Button
                                    size="small"
                                    variant="contained"
                                    component="label"
                                    className={cn(ss.dataDownload__download_btn)}
                                >
                                    <div className={cn(ss.dataDownload__download_btn_text)}>
                                        Данные в порядке TR
                                    </div>
                                    <input
                                        onChange={(e) => {
                                            this.onDataLoad(e, "fileOne")
                                        }}
                                        type="file"
                                        style={{display: "none"}}
                                    />
                                </Button>
                                <Button
                                    size="small"
                                    variant="contained"
                                    component="label"
                                    className={cn(ss.dataDownload__download_btn)}
                                >
                                    <div className={cn(ss.dataDownload__download_btn_text)}>
                                        Данные в порядке RT
                                    </div>
                                    <input
                                        onChange={(e) => {
                                            this.onDataLoad(e, "fileTwo")
                                        }}
                                        type="file"
                                        style={{display: "none"}}
                                    />
                                </Button>
                            </div>
                            <div className={cn(ss.dataDownload__download_file_texts)}>
                                <p className={cn(ss.dataDownload__download_file_text)}>
                                    <a className={cn(ss.customBold)}>Загружен файл:</a> {this.state.fileOneName}
                                </p>
                                <p className={cn(ss.dataDownload__download_file_text)}>
                                    <a className={cn(ss.customBold)}>Загружен файл:</a> {this.state.fileTwoName}
                                </p>
                            </div>
                        </div>
                    </Page>
                    );
                }
                else {
                    return (<Page
                        title="Загрузка данных"
                    >
                        Данные должны быть загружены в формате ".хlsx", ".хs" или ".сsv".
                        <br/>
                        <br/>
                        Необходима загрузка двух файлов.
                        <br/>
                        <br/>
                        Первый файл должен содержать данные с концентрацией тестового препарата в крови пациентов.
                        Второй файл должен содержать данные с концентрацией референсного препарата в крови пациентов.
                        <br/>
                        <br/>
                        Необходимо, чтобы в первой строке каждого файла был указан момент времени (в часах), в который
                        была
                        зафиксирована концентрация.
                        <br/>
                        <br/>
                        В первом столбце каждого файла нужно указать порядковый номер пациента.
                        <div className={cn(ss.dataDownload__download_btns_and_texts)}>
                            <div className={cn(ss.dataDownload__download_btns)}>
                                <Button
                                    size="small"
                                    variant="contained"
                                    component="label"
                                    className={cn(ss.dataDownload__download_btn)}
                                >
                                    <div className={cn(ss.dataDownload__download_btn_text)}>
                                        Тестовый препарат
                                    </div>
                                    <input
                                        onChange={(e) => {
                                            this.onDataLoad(e, "fileOne")
                                        }}
                                        type="file"
                                        style={{display: "none"}}
                                    />
                                </Button>
                                <Button
                                    size="small"
                                    variant="contained"
                                    component="label"
                                    className={cn(ss.dataDownload__download_btn)}
                                >
                                    <div className={cn(ss.dataDownload__download_btn_text)}>
                                        Референсный препарат
                                    </div>
                                    <input
                                        onChange={(e) => {
                                            this.onDataLoad(e, "fileTwo")
                                        }}
                                        type="file"
                                        style={{display: "none"}}
                                    />
                                </Button>
                            </div>
                            <div className={cn(ss.dataDownload__download_file_texts)}>
                                <p className={cn(ss.dataDownload__download_file_text)}>
                                    <a className={cn(ss.customBold)}>Загружен файл:</a> {this.state.fileOneName}
                                </p>
                                <p className={cn(ss.dataDownload__download_file_text)}>
                                    <a className={cn(ss.customBold)}>Загружен файл:</a> {this.state.fileTwoName}
                                </p>
                            </div>
                        </div>
                    </Page>
                    );
                }
            case 2:
                return (<Page
                    title="Выберите способ проверки данных на нормальность"
                >
                    <FormControl component="fieldset">
                        <RadioGroup
                            defaultValue={METHOD_OF_VERIFICATION[this.settings.method]}
                            name="radio-buttons-group"
                        >
                            {METHOD_OF_VERIFICATION.map((item, idx) => (
                                <FormControlLabel
                                    key={`m-${item}`}
                                    control={
                                        <Radio
                                            onClick={() => {
                                                this.selectRadio(idx, 'method');
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
                if (this.settings.plan == 0) {
                    return (
                        <Page
                            title="Выберите нужные таблицы"
                        >
                            <FormGroup>
                                {TABLE_SELECTION.map((item, idx) => (
                                    <FormControlLabel
                                        key={`m-${item}`}
                                        label={item}
                                        control={
                                            <Checkbox
                                                defaultChecked={this.settings.table[idx]}
                                                onClick={() => {
                                                    selectUnselectCheckbox(this, idx, 'table');
                                                }}
                                            />
                                        }
                                    />
                                ))}
                            </FormGroup>
                        </Page>
                    );
                } else {
                    return (<Page
                        title="Выберите таблицы"
                    >
                        <FormGroup>
                            {PARAL_TABLE_SELECTION.map((item, idx) => (
                                <FormControlLabel
                                    key={`m-${item}`}
                                    label={item}
                                    control={
                                        <Checkbox
                                            defaultChecked={this.settings.paral_table[idx]}
                                            onClick={() => {
                                                selectUnselectCheckbox(this, idx, 'paral_table');
                                            }}
                                        />
                                    }
                                />
                            ))}
                        </FormGroup>
                    </Page>);
                }
            case 4:
                if (this.settings.plan == 0) {
                    return (
                    <Page
                        title="Выберите графики для визуализации"
                    >
                        <FormGroup>
                            {VISUALIZATION_SELECTION.map((item, idx) => (
                                <FormControlLabel
                                    key={`m-${item}`}
                                    label={item}
                                    control={
                                        <Checkbox
                                            defaultChecked={this.settings.visualisation[idx]}
                                            onClick={() => {
                                                selectUnselectCheckbox(this, idx, 'visualisation');
                                            }}
                                        />
                                    }
                                />
                            ))}
                        </FormGroup>
                    </Page>
                );
                } else {
                    return (
                    <Page
                    title="Выберите способ проверки данных на однородность"
                >
                    <FormControl component="fieldset">
                        <RadioGroup
                            defaultValue={HOMOGENEITY_METHODS[this.settings.homogeneity_method]}
                            name="radio-buttons-group"
                        >
                            {HOMOGENEITY_METHODS.map((item, idx) => (
                                <FormControlLabel
                                    key={`m-${item}`}
                                    control={
                                        <Radio
                                            onClick={() => {
                                                this.selectRadio(idx, 'homogeneity_method');
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
                }
            case 5:
                return (
                    <Page
                        title="Выберите графики для визуализации"
                    >
                        <FormGroup>
                            {PARAL_GRAPHICS.map((item, idx) => (
                                <FormControlLabel
                                    key={`m-${item}`}
                                    label={item}
                                    control={
                                        <Checkbox
                                            defaultChecked={this.settings.paral_graphics[idx]}
                                            onClick={() => {
                                                selectUnselectCheckbox(this, idx, 'paral_graphics');
                                            }}
                                        />
                                    }
                                />
                            ))}
                        </FormGroup>
                    </Page>
                )
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
