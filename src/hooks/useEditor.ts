
import { Editor, EditorState, RichUtils, Transforms } from 'draft-js';
import { EditorView } from '@codemuse/editor';

export const useEditor = () => {
  const editorViewRef = React.useRef<EditorView | null>(null);

  return {
    editorView: editorViewRef.current,
    setEditorView: (view: EditorView) => editorViewRef.current = view,
    editorState: editorViewRef.current?.state,
    setEditorState: (state: EditorState) => editorViewRef.current?.onChange(state),
  };
};