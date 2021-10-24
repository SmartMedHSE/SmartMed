import * as React from 'react';

import { Container } from '@material-ui/core';

export const PAGES = {
    DescriptiveAnalysis: 1,
    Bioequivalence: 2,
    PredictiveAnalysis: 3,
};

export const MAIN_MENU = [
    {
        title: 'Описательный анализ',
        description: 'Получение обобщенной информации о данных, визуальный анализ',
        id: 'DescriptiveAnalysis',
    },
    {
        title: 'Биоэквивалентность',
        description: 'Исследование идентичности свойств биодоступности у исходного препарата и дженерика',
        id: 'Bioequivalence',
    },
    {
        title: 'Предсказательный анализ',
        description: 'Построение статистических и предсказательных моделей, ROC-анализ',
        id: 'PredictiveAnalysis',
    },
];

/**
 *
 * @param props: {onClick: (id: {string}) => void}
 * @returns {JSX.Element}
 * @constructor
 */
export const Menu = ({ onClick }) => (
    <div className="menu">
        <div className="menu__title">
            <h2>Выберете способ анализа</h2>
        </div>
        <form className="menu__items" noValidate>
            <ul>
                {MAIN_MENU.map((item) => (
                    <li key={item.id}>
                        <div className="menu__item">
                            <button
                                className="menu__button button button_size-xx button_color_grey"
                                onClick={() => onClick(item.id)}
                            >
                                {item.title}
                            </button>
                            <div className="menu__item-helper">{item.description}</div>
                        </div>
                    </li>
                ))}
            </ul>
        </form>
    </div>
);

export class App extends React.Component {

    state = {
        openPage: 0,
        error: false,
    };

    /**
     *
     * @param menuId {string}
     * @returns {JSX.Element}
     */
    detectPage(menuId) {
        const openPage = MAIN_MENU[menuId];
        this.setState({ openPage });
        switch (openPage) {
            case PAGES.DescriptiveAnalysis:
                return (
                    <div>
                    </div>
                );
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
                return <p>404 Page not found</p>;
        }
    }

    render() {
        return (
            <div className="main">
                <Container maxWidth="md">
                    <Menu onClick={this.detectPage}/>
                </Container>
            </div>
        );
    }
}