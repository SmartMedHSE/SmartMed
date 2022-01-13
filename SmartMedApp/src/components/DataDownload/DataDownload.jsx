import * as React from 'react';
import * as cn from 'classnames';

import {Button} from '@material-ui/core';

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
            <div className={cn(s.dataDownload__div)}>
                <Button
                    size="small"
                    variant="contained"
                    component="label"
                    className={cn(s.dataDownload__download_btn)}
                >
                    <div className={cn(s.dataDownload__download_btn_text)}>
                        Загрузить
                    </div>
                    <input
                        onChange={props.onLoad}
                        type="file"
                        style={{display: "none"}}
                        // style={{opacity: 0}}
                    />
                </Button>
            </div>
        </div>
    );
};