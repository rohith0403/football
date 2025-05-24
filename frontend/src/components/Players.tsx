import React, { useState, useEffect, useMemo } from 'react';

// Define the type for a single Player item
interface Player {
  id: number;
  name: string;
  nationality: string;
  attack: number;
  defense: number;
  midfield: number;
  position: string;
  // team: string; // Commented out as it's not in the current data structure
}

// Define the type for the API response based on your clarification
interface ApiResponse {
  content: Player[]; // The actual array of players is now inside 'content'
  totalElements: number; // Total number of elements across all pages
  totalPages: number; // Total number of pages (optional, can be calculated)
  size: number; // Number of elements per page
  number: number; // Current page number (often 0-indexed from backend)
  // You might have other properties here like 'first', 'last', 'empty', etc.
}

// Define the type for sort direction
type SortDirection = 'asc' | 'desc';

/**
 * Players Component
 * A functional React component that fetches and displays a sortable and paginated table of players.
 * It uses useState for managing component state (players, loading/error states, sorting, and pagination)
 * and useEffect for performing side effects (data fetching).
 */
const Players: React.FC = () => {
  // State to store the fetched players for the current page
  const [players, setPlayers] = useState<Player[]>([]);
  // State to manage the loading status
  const [loading, setLoading] = useState<boolean>(true);
  // State to store any error that might occur during fetching
  const [error, setError] = useState<string | null>(null);
  // State to store the currently sorted column key
  const [sortColumn, setSortColumn] = useState<keyof Player | null>(null);
  // State to store the current sort direction ('asc' for ascending, 'desc' for descending)
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');

  // Pagination states
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [itemsPerPage] = useState<number>(25); // Fixed number of items per page for demonstration
  const [totalPlayers, setTotalPlayers] = useState<number>(0); // Total number of players from the backend

  // Filter states (raw input values)
  const [nameInput, setNameInput] = useState<string>('');
  const [nationalityInput, setNationalityInput] = useState<string>('');
  const [positionFilter, setPositionFilter] = useState<string>('');

  // Debounced filter states (used for API calls)
  const [debouncedNameFilter, setDebouncedNameFilter] = useState<string>('');
  const [debouncedNationalityFilter, setDebouncedNationalityFilter] = useState<string>('');

  // Debounce effect for name filter
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedNameFilter(nameInput);
      setCurrentPage(1); // Reset page when filter changes
    }, 500); // 500ms debounce delay

    return () => {
      clearTimeout(handler);
    };
  }, [nameInput]);

  // Debounce effect for nationality filter
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedNationalityFilter(nationalityInput);
      setCurrentPage(1); // Reset page when filter changes
    }, 500); // 500ms debounce delay

    return () => {
      clearTimeout(handler);
    };
  }, [nationalityInput]);


  /**
   * useEffect Hook for Data Fetching
   * This hook runs when currentPage, itemsPerPage, or any debounced filter changes.
   * It performs the asynchronous data fetching operation for the current page with applied filters.
   */
  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        setLoading(true);
        setError(null);

        // Construct the URL with pagination and filter parameters
        // Assumes the backend API supports 'page' (0-indexed), 'size', 'name', 'nationality', and 'position' query parameters
        const queryParams = new URLSearchParams();
        queryParams.append('page', (currentPage - 1).toString());
        queryParams.append('size', itemsPerPage.toString());
        if (debouncedNameFilter) queryParams.append('name', debouncedNameFilter);
        if (debouncedNationalityFilter) queryParams.append('nationality', debouncedNationalityFilter);
        if (positionFilter) queryParams.append('position', positionFilter);

        const response = await fetch(`http://localhost:8080/players?${queryParams.toString()}`);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON response based on the new ApiResponse structure
        const result: ApiResponse = await response.json();

        // Update states with data from result.content and result.totalElements
        setPlayers(result.content);
        setTotalPlayers(result.totalElements); // Use totalElements for the total count
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPlayers();
  }, [currentPage, itemsPerPage, debouncedNameFilter, debouncedNationalityFilter, positionFilter]); // Dependencies for re-fetching data

  /**
   * handleSort Function
   * This function is called when a column header is clicked.
   * It updates the sortColumn and sortDirection states.
   * @param column The key of the column to sort by (e.g., 'id', 'name').
   */
  const handleSort = (column: keyof Player) => {
    // If the same column is clicked, toggle the sort direction
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // If a new column is clicked, set it as the sort column and default to ascending
      setSortColumn(column);
      setSortDirection('asc');
    }
  };

  /**
   * useMemo Hook for Sorted Players
   * This memoizes the sortedPlayers array. It will only re-calculate
   * when 'players', 'sortColumn', or 'sortDirection' change.
   * Note: Sorting is applied only to the players fetched for the current page,
   * as pagination is handled by the backend.
   */
  const sortedPlayers = useMemo(() => {
    // Create a shallow copy of the players array from the current page to avoid direct mutation
    const sortableItems = [...players];

    if (sortColumn) {
      sortableItems.sort((a, b) => {
        const aValue = a[sortColumn];
        const bValue = b[sortColumn];

        // Handle different data types for sorting
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          // Case-insensitive string comparison
          return sortDirection === 'asc'
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
        } else if (typeof aValue === 'number' && typeof bValue === 'number') {
          // Numeric comparison
          return sortDirection === 'asc'
            ? aValue - bValue
            : bValue - aValue;
        }
        // Fallback for other types or mixed types (shouldn't happen with Player interface)
        return 0;
      });
    }
    return sortableItems;
  }, [players, sortColumn, sortDirection]); // Dependencies for memoization

  // Calculate unique positions for the dropdown filter (nationality is now text input)
  const uniquePositions = useMemo(() => {
    const positions = new Set<string>();
    // It's generally better to get unique filter options from the backend or a separate endpoint
    // to ensure all possible options are available, not just those on the current page.
    // For this example, we'll continue to derive from current players for simplicity.
    players.forEach(player => positions.add(player.position));
    return Array.from(positions).sort();
  }, [players]);

  // Calculate total pages based on totalPlayers and itemsPerPage
  const totalPages = Math.ceil(totalPlayers / itemsPerPage);

  /**
   * handlePageChange Function
   * Updates the currentPage state, triggering a re-fetch of players for the new page.
   * @param pageNumber The page number to navigate to.
   */
  const handlePageChange = (pageNumber: number) => {
    if (pageNumber > 0 && pageNumber <= totalPages) {
      setCurrentPage(pageNumber);
    }
  };

  // Helper function to render sort indicator (arrow) next to column header
  const renderSortIndicator = (column: keyof Player) => {
    if (sortColumn === column) {
      return sortDirection === 'asc' ? ' ▲' : ' ▼'; // Up or down arrow
    }
    return ''; // No indicator
  };

  // Render the component UI
  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4 font-sans">
      <div className="bg-gray-800 p-8 rounded-lg shadow-xl w-full max-w-4xl">
        <h1 className="text-3xl font-bold text-center text-gray-100 mb-6">
          Players
        </h1>

        {/* Loading indicator */}
        {loading && (
          <div className="text-center text-blue-400 text-lg">
            Loading players...
          </div>
        )}

        {/* Error message display */}
        {error && (
          <div className="text-center text-red-400 text-lg">
            Error: {error}
          </div>
        )}

        {!loading && !error && (
          <>
            {/* Filter Controls */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div>
                <label htmlFor="nameFilter" className="block text-gray-300 text-sm font-bold mb-2">
                  Filter by Name:
                </label>
                <input
                  type="text"
                  id="nameFilter"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-700 text-gray-100 border-gray-600"
                  placeholder="Player name..."
                  value={nameInput} // Bind to raw input state
                  onChange={(e) => setNameInput(e.target.value)} // Update raw input state
                />
              </div>

              <div>
                <label htmlFor="nationalityFilter" className="block text-gray-300 text-sm font-bold mb-2">
                  Filter by Nationality:
                </label>
                <input
                  type="text"
                  id="nationalityFilter"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-700 text-gray-100 border-gray-600"
                  placeholder="Nationality..."
                  value={nationalityInput} // Bind to raw input state
                  onChange={(e) => setNationalityInput(e.target.value)} // Update raw input state
                />
              </div>

              <div>
                <label htmlFor="positionFilter" className="block text-gray-300 text-sm font-bold mb-2">
                  Filter by Position:
                </label>
                <select
                  id="positionFilter"
                  className="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-700 text-gray-100 border-gray-600"
                  value={positionFilter}
                  onChange={(e) => {
                    setPositionFilter(e.target.value);
                    setCurrentPage(1); // Reset to first page on filter change
                  }}
                >
                  <option value="">All Positions</option>
                  {uniquePositions.map((position) => (
                    <option key={position} value={position}>
                      {position}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="overflow-x-auto mb-8"> {/* Added mb-8 for spacing below the table */}
              <table className="min-w-full bg-gray-700 border border-gray-600 rounded-md">
                <thead>
                  <tr className="bg-gray-600 border-b border-gray-500">
                    {/* Table Headers with Sort functionality */}
                    <th
                      className="py-3 px-4 text-left text-sm font-semibold text-gray-200 uppercase tracking-wider rounded-tl-lg cursor-pointer hover:bg-gray-500"
                      onClick={() => handleSort('id')}
                    >
                      ID {renderSortIndicator('id')}
                    </th>
                    <th
                      className="py-3 px-4 text-left text-sm font-semibold text-gray-200 uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                      onClick={() => handleSort('name')}
                    >
                      Name {renderSortIndicator('name')}
                    </th>
                    <th
                      className="py-3 px-4 text-left text-sm font-semibold text-gray-200 uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                      onClick={() => handleSort('nationality')}
                    >
                      Nationality {renderSortIndicator('nationality')}
                    </th>
                    <th
                      className="py-3 px-4 text-left text-sm font-semibold text-gray-200 uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                      onClick={() => handleSort('attack')}
                    >
                      Attack {renderSortIndicator('attack')}
                    </th>
                    <th
                      className="py-3 px-4 text-left text-sm font-semibold text-gray-200 uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                      onClick={() => handleSort('defense')}
                    >
                      Defense {renderSortIndicator('defense')}
                    </th>
                    <th
                      className="py-3 px-4 text-left text-sm font-semibold text-gray-200 uppercase tracking-wider cursor-pointer hover:bg-gray-500"
                      onClick={() => handleSort('midfield')}
                    >
                      Midfield {renderSortIndicator('midfield')}
                    </th>
                    <th
                      className="py-3 px-4 text-left text-sm font-semibold text-gray-200 uppercase tracking-wider rounded-tr-lg cursor-pointer hover:bg-gray-500"
                      onClick={() => handleSort('position')}
                    >
                      Position {renderSortIndicator('position')}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {/* Map over the sortedPlayers array and render each player item as a table row */}
                  {sortedPlayers.map((player) => (
                    <tr key={player.id} className="border-b border-gray-600 last:border-b-0 hover:bg-gray-600">
                      <td className="py-3 px-4 text-sm text-gray-300">
                        {player.id}
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-300">
                        {player.name}
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-300">
                        {player.nationality}
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-300">
                        {player.attack}
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-300">
                        {player.defense}
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-300">
                        {player.midfield}
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-300">
                        {player.position}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination Controls */}
            <div className="flex justify-center items-center mt-6 space-x-2">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              {/* Render page numbers dynamically */}
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <button
                  key={page}
                  onClick={() => handlePageChange(page)}
                  className={`px-4 py-2 rounded-md ${
                    currentPage === page
                      ? 'bg-blue-800 text-white' // Active page style
                      : 'bg-gray-700 text-gray-200 hover:bg-gray-600' // Inactive page style
                  }`}
                >
                  {page}
                </button>
              ))}
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
            {/* Pagination summary text */}
            <p className="text-center text-gray-400 mt-4">
              Showing {players.length} of {totalPlayers} players. Page {currentPage} of {totalPages}.
            </p>
          </>
        )}
      </div>
    </div>
  );
};

export default Players;
