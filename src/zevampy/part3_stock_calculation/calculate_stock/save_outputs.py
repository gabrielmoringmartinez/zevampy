"""Save calculated stock datasets to disk."""

# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

from zevampy.load_data_and_prepare_inputs.dimension_names import stock_data_filename_label, stock_shares_filename_label


def save_outputs(stock_data, stock_shares, save_options, output_path):
    """
    Save calculated stock outputs to CSV files.

    This function saves vehicle stock data and, if available, stock-share data to the specified output directory.

    Parameters:
        stock_data (pandas.DataFrame):
            DataFrame containing calculated vehicle stock data.

        stock_shares (pandas.DataFrame or None):
            DataFrame containing calculated stock shares.

        save_options (dict):
            Dictionary containing output filenames.

        output_path (str):
            Directory where output files are saved.

    Returns:
        None
    """
    # Set default save options
    stock_data_filename = save_options.get(stock_data_filename_label)
    stock_shares_filename = save_options.get(stock_shares_filename_label)
    # Save stock data and stock shares if specified
    stock_data.to_csv(f'{output_path}/{stock_data_filename}', sep=',', index=False, decimal='.')
    if stock_shares is not None and stock_shares_filename:
        stock_shares.to_csv(f'{output_path}/{stock_shares_filename}', sep=',', index=False, decimal='.')
