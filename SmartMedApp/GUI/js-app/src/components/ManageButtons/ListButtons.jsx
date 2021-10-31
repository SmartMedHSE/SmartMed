import * as React from 'react';
import { Button } from '@material-ui/core';

/**
 *
 * @param props {{onClick: (isGoNext: boolean) => void}}
 * @returns {JSX.Element}
 * @constructor
 */
export const ListButtons = ({ onClick }) => {
    return (
        <div>
            <span>
                <Button variant="outlined" size="small" onClick={() => onClick(false)}>
                    Назад
                </Button>
                <Button variant="outlined" size="small" onClick={() => onClick(true)}>
                    Продолжить
                </Button>
            </span>
        </div>
    );
};