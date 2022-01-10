import * as React from 'react';
import {ListButtons} from '../ManageButtons';
import {Checkbox, FormControl, FormControlLabel, FormGroup, Input, Radio, RadioGroup} from '@material-ui/core';
import {fetchPost} from '../../utils';

const PLAN_SELECTION = [
    "Перекрёстный дизайн",
    "Параллельный дизайн"
];

const METHOD_OF_VERIFICATION = [
    "Критерий Колмогорова-Смирнова",
    "Критерий Шапиро-Уилка"
];

const TABLE_SELECTION = [
    "Средние площади под графиком по каждому препарату",
    "Результаты двухфакторного дисперсионного анализа",
    "Результаты оценки биоэквивалентности"
];

const VISUALIZATION_SELECTION = [
    "Индивидуальные графики для пациентов c концентрациями обоих препаратов",
    "Графики со средними концентрациями препаратов по группам",
    "График, где данные обобщены по двум препаратам"
];

const Page = (props) => (
    <div>
        <h2>{props.title}</h2>
        <div>{props?.description || ''}</div>
        {props.children}
    </div>
);

export class BioequivalenceAnalysis extends React.Component {

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
                void fetchPost('api/bioequivalence', this.settings);
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
                    title="Укажите, с какой выборкой проводится работа"
                >
                    <FormControl component="fieldset">
                        <RadioGroup name="radio-buttons-group">
                            {PLAN_SELECTION.map((item, idx) => (
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
            case 1:
                return (<Page
                    title="Загрузка данных"
                >
                    Данные должны быть загружены в формате ".хlsx"".хs" или ".сsv".
                    <br/>
                    <br/>
                    Необходима загрузка двух файлов.
                    <br/>
                    <br/>
                    Первый файл должен содержать информацию о пациентах, принимавших первым тестовый препарат, а за ним
                    - референсный. Второй файл должен содержать информацию о пациентах, которые сначала принимали
                    референсный препарат, затем - тестовый.
                    <br/>
                    <br/>
                    Необходимо, чтобы в первой строке каждого файла был указан момент времени (в часах), в который была
                    зафиксирована концентрация.
                    <br/>
                    <br/>
                    В первом столбце каждого файла нужно указать порядковый номер пациента.
                    <div>
                        <div>
                            <label htmlFor="fileOne">
                                Данные в порядке TR
                            </label>
                            <Input multiple type="file">
                                Загрузить
                            </Input>
                            <br/>
                            <label htmlFor="fileTwo">
                                Данные в порядке RT
                            </label>
                            <Input multiple type="file">
                                Загрузить
                            </Input>
                        </div>
                    </div>
                </Page>);
            case 2:
                return (<Page
                    title="Выберите способ проверки данных на нормальность"
                >
                    <FormControl component="fieldset">
                        <RadioGroup name="radio-buttons-group">
                            {METHOD_OF_VERIFICATION.map((item, idx) => (
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
                return (
                    <Page
                        title="Выберите нужные таблицы"
                    >
                        <FormGroup>
                            {TABLE_SELECTION.map((item, idx) => (
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
            case 4:
                return (
                    <Page
                        title="Выберите графики для визуализации"
                    >
                        <FormGroup>
                            {VISUALIZATION_SELECTION.map((item, idx) => (
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
