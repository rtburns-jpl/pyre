// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// code guard
#if !defined(pyre_grid_Tile_h)
#define pyre_grid_Tile_h

// declaration
template <typename indexT, typename layoutT>
class pyre::grid::Tile {
    // types
public:
    // for sizing things
    typedef std::size_t size_type;
    // aliases for my parts
    typedef indexT index_type;
    typedef layoutT layout_type;
    // slices
    typedef Slice<Tile> slice_type;
    // iterator
    typedef Iterator<index_type, layout_type> iterator_type;

    // meta-methods
public:
    Tile(index_type shape, layout_type layout);

    // interface
public:
    // accessors
    inline const auto & shape() const;
    inline const auto & layout() const;

    // the number of cells in this tile
    inline auto size() const;

    // compute the pixel offset implied by a given index
    // compute the index that corresponds to a given offset
    inline auto offset(const index_type & index) const;
    inline auto index(size_type offset) const;

    // syntactic sugar for the pair above
    inline auto operator[](const index_type & index) const;
    inline auto operator[](size_type offset) const;

    // iteration support
    inline auto begin() const;
    inline auto end() const;

    // iterating over slices in arbitrary order
    auto slice(const layout_type & order) const;
    auto slice(const index_type & begin, const index_type & end) const;
    auto slice(const index_type & begin, const index_type & end,
                     const layout_type & layout) const;

    // implementation details
private:
    const index_type _shape;
    const layout_type _layout;
};


#endif

// end of file