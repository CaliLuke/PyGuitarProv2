# guitarpro/models/__init__.py
# Re-export models from the sibling _models_definitions.py file

from .._models_definitions import (
    RepeatGroup, Clipboard, KeySignature, Song,
    LyricLine, Lyrics, Point, Padding, HeaderFooterElements,
    PageSetup, MidiChannel, DirectionSign, Tuplet, Duration,
    TimeSignature, TripletFeel, MeasureHeader, Color, Marker,
    TrackSettings, Track, GuitarString, MeasureClef, LineBreak,
    Measure, VoiceDirection, Voice, BeatStrokeDirection, BeatStroke,
    SlapEffect, BeatEffect, TupletBracket, BeatDisplay, Octave,
    BeatStatus, Beat, HarmonicEffect, NaturalHarmonic,
    ArtificialHarmonic, TappedHarmonic, PinchHarmonic, SemiHarmonic,
    GraceEffectTransition, Velocities, GraceEffect, TrillEffect,
    TremoloPickingEffect, SlideType, Fingering, NoteEffect, NoteType,
    Note, Chord, ChordType, Barre, ChordAlteration, ChordExtension,
    PitchClass, MixTableItem, WahEffect, MixTableChange,
    BendType, BendPoint, BendEffect, RSEMasterEffect, RSEEqualizer,
    Accentuation, RSEInstrument, TrackRSE, GPException
)

# Also re-export GPException if it's intended to be part of this package's public API
# from ..exceptions import GPException # Already imported via _models_definitions if it's there

__all__ = [
    'RepeatGroup', 'Clipboard', 'KeySignature', 'Song',
    'LyricLine', 'Lyrics', 'Point', 'Padding', 'HeaderFooterElements',
    'PageSetup', 'MidiChannel', 'DirectionSign', 'Tuplet', 'Duration',
    'TimeSignature', 'TripletFeel', 'MeasureHeader', 'Color', 'Marker',
    'TrackSettings', 'Track', 'GuitarString', 'MeasureClef', 'LineBreak',
    'Measure', 'VoiceDirection', 'Voice', 'BeatStrokeDirection', 'BeatStroke',
    'SlapEffect', 'BeatEffect', 'TupletBracket', 'BeatDisplay', 'Octave',
    'BeatStatus', 'Beat', 'HarmonicEffect', 'NaturalHarmonic',
    'ArtificialHarmonic', 'TappedHarmonic', 'PinchHarmonic', 'SemiHarmonic',
    'GraceEffectTransition', 'Velocities', 'GraceEffect', 'TrillEffect',
    'TremoloPickingEffect', 'SlideType', 'Fingering', 'NoteEffect', 'NoteType',
    'Note', 'Chord', 'ChordType', 'Barre', 'ChordAlteration', 'ChordExtension',
    'PitchClass', 'MixTableItem', 'WahEffect', 'MixTableChange',
    'BendType', 'BendPoint', 'BendEffect', 'RSEMasterEffect', 'RSEEqualizer',
    'Accentuation', 'RSEInstrument', 'TrackRSE', 'GPException'
]