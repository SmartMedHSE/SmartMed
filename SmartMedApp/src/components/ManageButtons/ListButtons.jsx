import * as React from 'react';
import * as cn from 'classnames';

import {Button} from '@material-ui/core';

import * as s from './ListButtons.scss';

/**
 *
 * @param props {{onClick: (isGoNext: boolean) => void}}
 * @returns {JSX.Element}
 * @constructor
 */
export const ListButtons = ({onClick, nextText}) => {
    return (
        <div className={s.listButtons}>
            <span>
                <Button className={cn(s.listButtons__btn)} size="small"
                        onClick={() => onClick(false)}>
                    Назад
                </Button>
                <Button className={cn(s.listButtons__btn)} size="small"
                        onClick={() => onClick(true)}>
                    {nextText()}
                </Button>
            </span>
        </div>
    );
};