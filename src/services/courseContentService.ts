import { supabase } from '../lib/supabase';

export interface CourseContent {
  id: string;
  node_id: string;
  title: string;
  overview: string;
  learning_objectives: string[];
  estimated_time: number;
  difficulty_level: string;
  sections?: CourseSection[];
  resources?: CourseResource[];
  key_concepts?: KeyConcept[];
  learning_tips?: LearningTip[];
}

export interface CourseSection {
  id: string;
  content_id: string;
  section_order: number;
  section_type: 'introduction' | 'concept' | 'example' | 'practice' | 'summary';
  title: string;
  content: string;
  media_url?: string;
  media_type?: 'image' | 'video' | 'diagram' | 'code';
  interactive_elements?: any[];
}

export interface CourseResource {
  id: string;
  content_id: string;
  resource_type: 'video' | 'article' | 'exercise' | 'documentation';
  title: string;
  description?: string;
  url?: string;
  is_required: boolean;
}

export interface KeyConcept {
  id: string;
  content_id: string;
  term: string;
  definition: string;
  example?: string;
}

export interface LearningTip {
  id: string;
  content_id: string;
  tip_type: 'general' | 'warning' | 'best_practice' | 'common_mistake';
  content: string;
}

export class CourseContentService {
  /**
   * Get course content for a specific node
   */
  static async getContentForNode(nodeId: string): Promise<CourseContent | null> {
    try {
      // Fetch main content
      const { data: contentData, error: contentError } = await supabase
        .from('course_content')
        .select('*')
        .eq('node_id', nodeId)
        .single();

      if (contentError || !contentData) {
        console.log(`No content found for node ${nodeId}`);
        return null;
      }

      // Fetch sections
      const { data: sections } = await supabase
        .from('course_sections')
        .select('*')
        .eq('content_id', contentData.id)
        .order('section_order', { ascending: true });

      // Fetch resources
      const { data: resources } = await supabase
        .from('course_resources')
        .select('*')
        .eq('content_id', contentData.id)
        .order('is_required', { ascending: false });

      // Fetch key concepts
      const { data: keyConcepts } = await supabase
        .from('key_concepts')
        .select('*')
        .eq('content_id', contentData.id);

      // Fetch learning tips
      const { data: learningTips } = await supabase
        .from('learning_tips')
        .select('*')
        .eq('content_id', contentData.id);

      return {
        ...contentData,
        sections: sections || [],
        resources: resources || [],
        key_concepts: keyConcepts || [],
        learning_tips: learningTips || []
      };
    } catch (error) {
      console.error('Error fetching course content:', error);
      return null;
    }
  }

  /**
   * Create or update course content
   */
  static async upsertContent(nodeId: string, content: Partial<CourseContent>): Promise<boolean> {
    try {
      const { data, error } = await supabase
        .from('course_content')
        .upsert({
          node_id: nodeId,
          title: content.title,
          overview: content.overview,
          learning_objectives: content.learning_objectives,
          estimated_time: content.estimated_time,
          difficulty_level: content.difficulty_level,
          updated_at: new Date().toISOString()
        }, {
          onConflict: 'node_id'
        })
        .select()
        .single();

      if (error) {
        console.error('Error upserting content:', error);
        return false;
      }

      return true;
    } catch (error) {
      console.error('Error in upsertContent:', error);
      return false;
    }
  }

  /**
   * Add a section to course content
   */
  static async addSection(contentId: string, section: Omit<CourseSection, 'id' | 'content_id'>): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('course_sections')
        .insert({
          content_id: contentId,
          ...section
        });

      return !error;
    } catch (error) {
      console.error('Error adding section:', error);
      return false;
    }
  }

  /**
   * Update section order
   */
  static async updateSectionOrder(sectionId: string, newOrder: number): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('course_sections')
        .update({ section_order: newOrder })
        .eq('id', sectionId);

      return !error;
    } catch (error) {
      console.error('Error updating section order:', error);
      return false;
    }
  }

  /**
   * Add a resource to course content
   */
  static async addResource(contentId: string, resource: Omit<CourseResource, 'id' | 'content_id'>): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('course_resources')
        .insert({
          content_id: contentId,
          ...resource
        });

      return !error;
    } catch (error) {
      console.error('Error adding resource:', error);
      return false;
    }
  }

  /**
   * Add a key concept
   */
  static async addKeyConcept(contentId: string, concept: Omit<KeyConcept, 'id' | 'content_id'>): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('key_concepts')
        .insert({
          content_id: contentId,
          ...concept
        });

      return !error;
    } catch (error) {
      console.error('Error adding key concept:', error);
      return false;
    }
  }

  /**
   * Add a learning tip
   */
  static async addLearningTip(contentId: string, tip: Omit<LearningTip, 'id' | 'content_id'>): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('learning_tips')
        .insert({
          content_id: contentId,
          ...tip
        });

      return !error;
    } catch (error) {
      console.error('Error adding learning tip:', error);
      return false;
    }
  }

  /**
   * Delete a section
   */
  static async deleteSection(sectionId: string): Promise<boolean> {
    try {
      const { error } = await supabase
        .from('course_sections')
        .delete()
        .eq('id', sectionId);

      return !error;
    } catch (error) {
      console.error('Error deleting section:', error);
      return false;
    }
  }

  /**
   * Get all content summaries (for admin)
   */
  static async getAllContentSummaries(): Promise<any[]> {
    try {
      const { data, error } = await supabase
        .from('course_content')
        .select('id, node_id, title, estimated_time, updated_at')
        .order('updated_at', { ascending: false });

      if (error) throw error;
      return data || [];
    } catch (error) {
      console.error('Error fetching content summaries:', error);
      return [];
    }
  }

  /**
   * Check if node has content
   */
  static async nodeHasContent(nodeId: string): Promise<boolean> {
    try {
      const { data, error } = await supabase
        .from('course_content')
        .select('id')
        .eq('node_id', nodeId)
        .single();

      return !!data && !error;
    } catch (error) {
      return false;
    }
  }
}