# Valgrind XML-to-SARIF Converter

## Summary

A GitHub Action for analyzing your memory management using [Valgrind](https://valgrind.org) and CodeQL

## Example:
```yml
name: Valgrind

on:
jobs:
  valgrind:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code

      - name: Build code
        ...

      - name: Run Valgrind
        run: |
          valgrind \
          ...
          --xml=yes --xml-file=valgrind-output.xml \
          ./build-${{ matrix.ssl }}/bin/umurmurd -c umurmur.conf.example -h

      - name: Convert XML to SARIF
        uses: troxor/valgrind-sarif-action@v0.0.1
        with:
          # Output from Valgrind
          xml_input_file: valgrind-output.xml
          # Input to upload step
          sarif_output_file: valgrind-output.sarif

      - name: Upload SARIF file
        uses: github/codeql-action/upload-sarif@v3
        with:
          # Path to SARIF file relative to the root of the repository
          sarif_file: valgrind-output.sarif
          category: valgrind
```
