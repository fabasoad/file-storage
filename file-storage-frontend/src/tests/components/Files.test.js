import React from 'react';
import { shallow } from 'enzyme';
import Files from '../../components/Files';

let wrapperWithFiles, wrapperWithoutFiles, expectedFiles, handleDeleteFiles;

const createFileObject = (fileName, index, handleDeleteFile) => ({
    file: fileName,
    index: index,
    handleDeleteFile: handleDeleteFile
});

beforeEach(() => {
    const handleDeleteFile = jest.fn();
    expectedFiles = [
        createFileObject('file1', 1, handleDeleteFile),
        createFileObject('file2', 2, handleDeleteFile)
    ];
    handleDeleteFiles = jest.fn();
    wrapperWithFiles = shallow(<Files
        files={expectedFiles}
        handleDeleteFiles={handleDeleteFiles}
        handleDeleteFile={handleDeleteFile}
    />);
    wrapperWithoutFiles = shallow(<Files
        files={[]}
        handleDeleteFiles={handleDeleteFiles}
        handleDeleteFile={handleDeleteFile}
    />);
});

test('should render empty Files correctly', () => {
    expect(wrapperWithoutFiles).toMatchSnapshot();
});

test('should render not empty Files correctly', () => {
    expect(wrapperWithFiles).toMatchSnapshot();
});

test('should handle handleDeleteFiles', () => {
    wrapperWithoutFiles.find('button').prop('onClick')();
    expect(handleDeleteFiles).toHaveBeenCalledTimes(1);
});