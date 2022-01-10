import * as React from 'react';
import * as cn from 'classnames';

import {Input} from '@material-ui/core';

import * as s from './DataDownload.scss';

/**
 * @param props {{onLoad: (filePath) => void}}
 * @returns {JSX.Element}
 * @constructor
 */
export const DataDownload = (props) => {
    return (
        <div className={s.dataDownload}>
            <div className={cn(s.dataDownload__download_text)}>
                Для того, чтобы выполнить загрузку данных, кликните на кнопку ниже.
                В открывающемся окне выберите файл в формате "xlsx", "csv", "tsv"
            </div>
            <div>
                <label for="file">
                    <i></i> Custom Upload
                </label>
                <Input className={cn(s.dataDownload__input)} multiple type="file"
                       onChange={props.onLoad}>Загрузить</Input>
                {/* <Button variant="contained" component="span">*/}
                {/* Загрузить */}
                {/*</Button> */}
            </div>
        </div>
    );
};