import React, { useEffect, useMemo, useState } from 'react';

interface Player {
  id: number;
  name: string;
  nationality: string;
  attack: number;
  defense: number;
  midfield: number;
  position: string;
}

interface ApiResponse {
  content: Player[];
  totalElements: number;
  totalPages: number;
  size: number;
  number: number;
}

type SortDirection = 'asc' | 'desc';

/**
 * Players Component
 * Placeholder component for displaying player information.
 */
const Players: React.FC = () => {

  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [sortColumn, setSortColumn] = useState<keyof Player | null>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [itemsPerPage] = useState<number>(25);
  const [totalPlayers, setTotalPlayers] = useState<number>(0);


  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        setLoading(true);
        setError(null);

        const queryParams = new URLSearchParams();
        queryParams.append('page', (currentPage - 1).toString());
        queryParams.append('size', itemsPerPage.toString());

        // IMPORTANT: Replace 'http://localhost:8080/players' with your actual API endpoint
        // This URL is a placeholder and will not work without a running backend server.
        const response = await fetch(`http://localhost:8080/players?${queryParams.toString()}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const result: ApiResponse = await response.json();
        setPlayers(result.content);
        setTotalPlayers(result.totalElements);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPlayers();
  }, [currentPage, itemsPerPage]);

  const handleSort = (column: keyof Player) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortDirection('asc');
    }
  };

  const sortedPlayers = useMemo(() => {
    const sortableItems = [...players];
    if (sortColumn) {
      sortableItems.sort((a, b) => {
        const aValue = a[sortColumn];
        const bValue = b[sortColumn];
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          return sortDirection === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
        } else if (typeof aValue === 'number' && typeof bValue === 'number') {
          return sortDirection === 'asc' ? aValue - bValue : bValue - aValue;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [players, sortColumn, sortDirection]);


  const totalPages = Math.ceil(totalPlayers / itemsPerPage);

  const handlePageChange = (pageNumber: number) => {
    if (pageNumber > 0 && pageNumber <= totalPages) {
      setCurrentPage(pageNumber);
    }
  };

  const renderSortIndicator = (column: keyof Player) => {
    if (sortColumn === column) {
      return sortDirection === 'asc' ? ' ▲' : ' ▼';
    }
    return '';
  };

  return (
    // This component now manages its own full-screen background and centering
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4 font-sans">
      <div className="bg-gray-800 p-8 rounded-xl shadow-2xl w-full max-w-4xl">
        <h1 className="text-3xl font-bold text-center text-gray-100 mb-6">Players</h1>
        {loading && <div className="text-center text-blue-400 text-lg">Loading players...</div>}
        {error && <div className="text-center text-red-400 text-lg">Error: {error}</div>}
        {!loading && !error && (
          <>
            <div className="overflow-x-auto"> {/* Removed mb-8 from here */}
              <table className="min-w-full bg-gray-700 border border-gray-600 rounded-md">
                <thead>
                  <tr className="bg-gray-600 border-b border-gray-500">
                    <th className="py-3 px-4 text-left text-sm font-semibold text-gray-200 cursor-pointer hover:bg-gray-500" onClick={() => handleSort('id')}>ID{renderSortIndicator('id')}</th>
                    <th className="py-3 px-4 text-left text-sm font-semibold text-gray-200 cursor-pointer hover:bg-gray-500" onClick={() => handleSort('name')}>Name{renderSortIndicator('name')}</th>
                    <th className="py-3 px-4 text-left text-sm font-semibold text-gray-200 cursor-pointer hover:bg-gray-500" onClick={() => handleSort('nationality')}>Nationality{renderSortIndicator('nationality')}</th>
                    <th className="py-3 px-4 text-left text-sm font-semibold text-gray-200 cursor-pointer hover:bg-gray-500" onClick={() => handleSort('attack')}>Attack{renderSortIndicator('attack')}</th>
                    <th className="py-3 px-4 text-left text-sm font-semibold text-gray-200 cursor-pointer hover:bg-gray-500" onClick={() => handleSort('defense')}>Defense{renderSortIndicator('defense')}</th>
                    <th className="py-3 px-4 text-left text-sm font-semibold text-gray-200 cursor-pointer hover:bg-gray-500" onClick={() => handleSort('midfield')}>Midfield{renderSortIndicator('midfield')}</th>
                    <th className="py-3 px-4 text-left text-sm font-semibold text-gray-200 cursor-pointer hover:bg-gray-500" onClick={() => handleSort('position')}>Position{renderSortIndicator('position')}</th>
                  </tr>
                </thead>
                <tbody>
                  {sortedPlayers.map((player) => (
                    <tr key={player.id} className="border-b border-gray-600 hover:bg-gray-600">
                      <td className="py-3 px-4 text-sm text-gray-300">{player.id}</td>
                      <td className="py-3 px-4 text-sm text-gray-300">{player.name}</td>
                      <td className="py-3 px-4 text-sm text-gray-300">{player.nationality}</td>
                      <td className="py-3 px-4 text-sm text-gray-300">{player.attack}</td>
                      <td className="py-3 px-4 text-sm text-gray-300">{player.defense}</td>
                      <td className="py-3 px-4 text-sm text-gray-300">{player.midfield}</td>
                      <td className="py-3 px-4 text-sm text-gray-300">{player.position}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className="min-w-full flex justify-center items-center pt-4 mt-4 border-t border-gray-700 space-x-2 overflow-x-scroll"> {/* Added pt-4, mt-4, border-t, border-gray-700 */}
                <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1} className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50">Previous</button>
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                  <button key={page} onClick={() => handlePageChange(page)} className={`px-4 py-2 rounded-md ${currentPage === page ? 'bg-blue-800 text-white' : 'bg-gray-700 text-gray-200 hover:bg-gray-600'}`}>{page}</button>
                ))}
                <button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages} className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50">Next</button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};




export default Players;
