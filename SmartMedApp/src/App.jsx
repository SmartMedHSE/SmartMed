import * as React from 'react';

import {Container} from '@material-ui/core';

import {DescriptiveAnalysis} from './components/DescriptiveAnalysis';
import {BioequivalenceAnalysis} from './components/Bioequivalence';
import {PredictiveAnalysis} from './components/PredictiveAnalysis';
import {ComparativeAnalysis} from './components/ComparativeAnalysis';
import {ClusterAnalysis} from './components/ClusterAnalysis';

import {Menu} from './components/Menu';

import './styles/_styles.scss';

export const PAGES = {
    DescriptiveAnalysis: 1,
    BioequivalenceAnalysis: 2,
    PredictiveAnalysis: 3,
    ComparativeAnalysis: 4,
    // ClusterAnalysis: 5
};

export class App extends React.Component {

    state = {
        openPage: 0,
        error: false,
    };

    /**
     * @returns {JSX.Element}
     */
    detectPage = () => {
        const {openPage} = this.state;
        switch (openPage) {
            case PAGES.DescriptiveAnalysis:
                return <DescriptiveAnalysis onExit={() => this.setState({openPage: 0})}/>;
            case PAGES.BioequivalenceAnalysis:
                return <BioequivalenceAnalysis onExit={() => this.setState({openPage: 0})}/>;
            case PAGES.PredictiveAnalysis:
                return <PredictiveAnalysis onExit={() => this.setState({openPage: 0})}/>;
            case PAGES.ComparativeAnalysis:
                return <ComparativeAnalysis onExit={() => this.setState({openPage: 0})}/>;
            // case PAGES.ClusterAnalysis:
            //     return <ClusterAnalysis onExit={() => this.setState({openPage: 0})}/>;
            default:
                return (
                    <Menu
                        onClick={(menuId) => {
                            if (PAGES.hasOwnProperty(menuId)) {
                                this.setState({openPage: PAGES[menuId]});
                            }
                        }}
                    />
                );
        }
    };

    render() {
        const {openPage} = this.state;
        return (
            <div className="main">
                <Container maxWidth="md">
                    {this.detectPage()}
                </Container>
            </div>
        );
    }
}