import * as React from 'react';

import { DataDownload } from '../DataDownload';
import { ListButtons } from '../ManageButtons';
import { DataPreparation } from './DataPreparation.jsx';

const DATA_PREP_OPTIONS = [ 'Средним/модой (численные/категориальные значения)',
    'Введенным значением (требуется ввод для каждого столбца отдельно)',
    'Удаление строк с пропущенными значениями',
    'Медианной/модой (численные/категориальные значения)'
];

export class DescriptiveAnalysis extends React.Component {

    state = {
        currentPage: 0,
        maxPage: 3,
        dataPrepOptionId: -1,
    };

    paginate = (goNext) => {
        const { currentPage, maxPage } = this.state;
        if (goNext) {
            if (currentPage < maxPage) {
                this.setState({ currentPage: currentPage + 1 });
            }
        } else {
            if (currentPage > 0) {
                this.setState({ currentPage: currentPage - 1 });
            } else {
                this.props.onExit();
            }
        }
    };

    selectDataPrepType = (id) => this.setState({ dataPrepOptionId: id });

    openCurrentPage = () => {
        const { currentPage } = this.state;
        switch (currentPage) {
            case 0:
                return <DataDownload onLoad={() => null}/>;
            case 1:
                return <DataPreparation onClick={this.selectDataPrepType} options={DATA_PREP_OPTIONS}/>;
            default:
                console.error(`unknown page: ${currentPage}`);
        }
    };

    render() {
        return (
            <div className="desc">
                {this.openCurrentPage()}
                <ListButtons onClick={this.paginate}/>
            </div>
        );
    }

}
