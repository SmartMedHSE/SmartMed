import * as React from 'react';

import {Container} from '@material-ui/core';

import {DescriptiveAnalysis} from './components/DescriptiveAnalysis';
import {Menu} from './components/Menu';

import './styles/_styles.scss';

export const PAGES = {
    DescriptiveAnalysis: 1,
    Bioequivalence: 2,
    PredictiveAnalysis: 3,
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
            case PAGES.Bioequivalence:
                return (
                    <div>
                    </div>
                );
            case PAGES.PredictiveAnalysis:
                return (
                    <div>
                    </div>
                );
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