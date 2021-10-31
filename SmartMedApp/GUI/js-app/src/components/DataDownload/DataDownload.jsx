import * as React from 'react';

import { Button, Input } from '@material-ui/core';

const onLoad = () => {
}

/**
 * @param props {{onLoad: (data) => void}}
 * @returns {JSX.Element}
 * @constructor
 */
export const DataDownload = (props) => {
    return (
        <div>
            <h2>Загрузите данные</h2>
            <div>
                Для того, чтобы выполнить загрузку данных, кликните на кнопку ниже.
                В открывающемся окне выберите файл в формате "xlsx", "csv", "tsv"
            </div>
            <div>
                <Input multiple type="file">Загрузить</Input>
                {/*<Button variant="contained" component="span">*/}
                {/*    Загрузить*/}
                {/*</Button>*/}
            </div>
        </div>
    );
};