import * as React from 'react';

import {fetchPost} from "../../utils";

import {ListButtons} from "../ManageButtons";

// import * as s from './MultipleRegression.scss';
import {DataPreparation} from "../DataPreparation/DataPreparation.jsx";
import {Checkbox, FormControlLabel, FormGroup} from "@material-ui/core";

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

export class MultipleRegression extends React.Component {

    state = {
        currentPage: 0,
        maxPage: 4,
        dataPrepOptionId: -1,
        nextText: "Продолжить",
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

    getNextText = () => {
        if (this.state.currentPage < this.state.maxPage) {
            return "Продолжить";
        } else {
            return "Завершить";
        }
    };

    openCurrentPage = () => {
        const {currentPage} = this.state;
        switch (currentPage) {
            case 0:
                return (
                    <Page title="Выберите зависимую переменную из списка">
                        <DataPreparation onClick={this.selectDataPrepType}
                                         options={DEPENDENT_PARAMS_OPTIONS}
                        />
                    </Page>
                );
            case 1:
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
                <ListButtons onClick={this.paginate} nextText={this.getNextText}/>
            </div>
        );
    }

}